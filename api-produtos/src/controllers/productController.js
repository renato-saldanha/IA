// Controller: recebe requisições, chama o service e trata respostas
const { validationResult } = require('express-validator');
const service = require('../services/productService');

function handleValidation(req) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    const err = new Error('Dados inválidos');
    err.status = 400;
    err.details = errors.array();
    throw err;
  }
}

module.exports = {
  async list(req, res, next) {
    try {
      const items = await service.listAll();
      res.json(items);
    } catch (err) { next(err); }
  },

  async get(req, res, next) {
    try {
      const item = await service.getById(req.params.id);
      if (!item) return res.status(404).json({ message: 'Produto não encontrado' });
      res.json(item);
    } catch (err) { next(err); }
  },

  async create(req, res, next) {
    try {
      handleValidation(req);
      const created = await service.create(req.body);
      res.status(201).json(created);
    } catch (err) { next(err); }
  },

  async update(req, res, next) {
    try {
      handleValidation(req);
      const updated = await service.update(req.params.id, req.body);
      res.json(updated);
    } catch (err) { next(err); }
  },

  async remove(req, res, next) {
    try {
      await service.remove(req.params.id);
      res.status(204).send();
    } catch (err) { next(err); }
  }
};