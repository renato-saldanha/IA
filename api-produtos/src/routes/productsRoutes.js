
// Rotas de produtos com validações usando express-validator
const express = require('express');
const { body, param } = require('express-validator');
const controller = require('../controllers/productController');

const router = express.Router();

// Validações para criação/edição
const productValidators = [
  body('name')
    .exists().withMessage('name é obrigatório')
    .isString().withMessage('name deve ser string')
    .isLength({ min: 3 }).withMessage('name deve ter pelo menos 3 caracteres'),
  body('price')
    .exists().withMessage('price é obrigatório')
    .isFloat({ gt: 0 }).withMessage('price deve ser número maior que 0'),
  body('stock')
    .optional()
    .isInt({ min: 0 }).withMessage('stock deve ser inteiro >= 0'),
  body('description')
    .optional()
    .isString().withMessage('description deve ser string')
];

// Rotas CRUD
router.get('/', controller.list);
router.get('/:id', controller.get);
router.post('/', productValidators, controller.create);
router.put('/:id', productValidators, controller.update);
router.delete('/:id', controller.remove);

module.exports = router;