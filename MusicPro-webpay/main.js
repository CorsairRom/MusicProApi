const axios = require('axios');
const express = require('express');
const WebpayPlus = require("transbank-sdk").WebpayPlus;
const { Options, IntegrationApiKeys, Environment, IntegrationCommerceCodes } = require("transbank-sdk");

const app = express();
const port = 3000 || process.env.PORT;

app.use(express.json());

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
        
        const tx = new WebpayPlus.Transaction(new Options(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, Environment.Integration));
        const response = await tx.create(
            compra.id.toString(),
            "S" + Math.floor(Math.random() * 1000),
            compra.total,
            "http://localhost:3000/confirmacion"
          );

        console.log(response.url + "?token_ws=" + response.token )
        res.json("La compra se esta llevando a cabo en: " + response.url + "?token_ws=" + response.token )
      } catch (error) {
        console.error('Error:', error.message);
        res.status(500).send('Error:', error.message);
      }
});

app.get('/confirmacion', async (req, res) => {
  try {
      const token = req.query.token_ws;

      const tx = new WebpayPlus.Transaction(new Options(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, Environment.Integration));
      const response = await tx.commit(token);    

      if (response.status == 'AUTHORIZED') {
        console.log(response)
        res.status(200).send('La compra se ha concretado de forma exitosa :D');
        // enviar por axios el id del pedido a la api de django
      } else {
        res.status(400).send('Algo ha salido mal :c');
      }
    } catch (error) {
      console.error('Error:', error.message);
      res.status(500).send('Error:', error.message);
    }
});

app.listen(port, ()=>{
    console.log('la pagina ha funcionado en: http://localhost:' + port);
})