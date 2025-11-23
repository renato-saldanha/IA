// Camada de serviço: lógica de negócio sobre produtos
const repository = require('../repositories/productRepository');

module.exports = {
  async listAll() {
    return await repository.getAll();
  },

  async getById(id) {
    return await repository.getById(id);
  },

  async create(product) {
    // Evita produto com mesmo nome
    const exists = await repository.findByName(product.name);
    if (exists) {
      const err = new Error('Já existe um produto com esse nome');
      err.status = 400;
      throw err;
    }
    return await repository.create(product);
  },

  async update(id, fields) {
    // Se alterar nome, evitar duplicatas
    if (fields.name) {
      const existing = await repository.findByName(fields.name);
      if (existing && existing.id !== id) {
        const err = new Error('Outro produto já usa esse nome');
        err.status = 400;
        throw err;
      }
    }
    const updated = await repository.update(id, fields);
    if (!updated) {
      const err = new Error('Produto não encontrado');
      err.status = 404;
      throw err;
    }
    return updated;
  },

  async remove(id) {
    const ok = await repository.remove(id);
    if (!ok) {
      const err = new Error('Produto não encontrado');
      err.status = 404;
      throw err;
    }
    return;
  }
};