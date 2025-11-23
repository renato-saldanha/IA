const express = require('express');
const productsRouter = require('./routes/productsRoutes');

const app = express();
app.use(express.json());
app.use('/products', productsRouter);
app.get('/', (req, res) => {res.send('API de produtos rodando!');});

// Middleware de erro (deve estar após rotas)
app.use((err, req, res, next) => {
  // Se err.status definido pelo service, usa; senão 500
  const status = err.status || 500;
  const payload = { message: err.message || 'Erro interno' };
  if (err.details) payload.details = err.details; // detalhes de validação
  res.status(status).json(payload);
});

module.exports = app;