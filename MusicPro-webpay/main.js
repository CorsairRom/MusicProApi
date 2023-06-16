const axios = require('axios');
const express = require('express');
const WebpayPlus = require("transbank-sdk").WebpayPlus;
const { Options, IntegrationApiKeys, Environment, IntegrationCommerceCodes } = require("transbank-sdk");

const app = express();
const port = 3000 || process.env.PORT;

app.use(express.json()); // Middleware to parse JSON request bodies

app.get('/', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/pedido');
        res.json(response.data);
        
      } catch (error) {
        console.error('Error retrieving users:', error.message);
        res.status(500).send('Error retrieving users');
      }
});



  app.post('/comprar', async (req, res) => {
      try {
          let compra = req.body;
          let detalleExists = false;

          const values = await axios.get('http://127.0.0.1:8000/api/pedido');
          values.data.forEach(element => {
              if (element.id == compra.id) {
                  compra = element
                  detalleExists = true;                   
              }
          });

          
          
          if (!detalleExists) {
              throw new Error("No existe un pedido con el id indicado.")
          }
          
          // Send request to Webpay API
          const tx = new WebpayPlus.Transaction(new Options(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, Environment.Integration));
          const response = await tx.create(
              compra.id.toString(),
              "S" + Math.floor(Math.random() * 1000),
              compra.subtotal,
              "http://localhost:3000/confirmacion"
            );

          res.json("La compra se esta llevando a cabo en: " + response.url + "?token_ws=" + response.token )
        } catch (error) {
          res.status(500).send('Error:' + error.message);
        }
  });

app.get('/confirmacion', async (req, res) => {
  try {
      const token = req.query.token_ws;

      const tx = new WebpayPlus.Transaction(new Options(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, Environment.Integration));
      const response = await tx.commit(token);    

      if (response.status == 'AUTHORIZED') {
        res.status(200).send('La compra se ha concretado de forma exitosa :D');
      } else {
        res.status(200).send('La compra no se ha autorizado');
      }
    } catch (error) {
      console.error('Error a:', error.message);
      res.status(500).send('Error a:' + error.message);
    }
});



app.listen(port, ()=>{
    console.log('la pagina ha funcionado en: http://localhost:' + port);
})

// descomentar para testing
// module.exports = app;