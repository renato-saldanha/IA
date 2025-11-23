const fs  = require('fs').promises;
const path = require('path');
const {v4: uuidv4} = require('uuid');

const dbPath = path.join(__dirname, '../data/products.json');

async function readFile() {
    try {
        const content = await fs.readFile(dbPath, 'utf-8');
        return JSON.parse(content);
    } catch (error) {
        return [];
    }
}

async function writeFile(data) {
    await fs.writeFile(dbPath, JSON.stringify(data, null, 2), 'utf8');
}

module.exports = {
    async getAll() {
        return await readFile();
    },
    
    async getById(id) {
        const products = await readFile();
        return products.find(product => product.id === id) || null;
    },

    async findByName(name) {
        const products = await readFile();
        return products.find(p => p.name && String(p.name).toLowerCase() === String(name).toLowerCase()) || null;
    },

    async create(product) {
        const products = await readFile();
        const newProduct = { id: uuidv4(), ...product };
        products.push(newProduct);
        await writeFile(products);
        return newProduct;             
    },

    async update(id, updatedProduct) {
        const products = await readFile();
        const index = products.findIndex(product => product.id === id);
        if (index === -1) return null;
        products[index] = { ...products[index], ...updatedProduct };
        await writeFile(products);
        return products[index];
    },

    async remove(id) {
        const products = await readFile();
        const filtered = products.filter(product => product.id !== id);
        if (filtered.length === products.length) return false;
        await writeFile(filtered);
        return true;
    }
}