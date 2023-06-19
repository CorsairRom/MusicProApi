const request = require('supertest');
const app = require('./main');

// Add the following code at the end of the test file to start the server
const server = app.listen(3000, () => {
  console.log('Server started for testing');
});

describe('POST /comprar', () => {
  // we define our first test case
  describe('Giving an id for a "detalle"', () => {
    test ("if the data is valid, should respond with a 200 status", async () => {
      const response = await request(app).post("/comprar").send({
        id: 1
      });

      await expect(response.statusCode).toBe(200);
    });

    test ("if the data is valid, should respond with a json type as the transaction URL", async () => {
      const response = await request(app).post("/comprar").send({
        id: 2
      });

      await expect(response.headers['content-type']).toEqual(expect.stringContaining("json"));
    });

    test ("if the data dont exists, should respond with a 500 status", async () => {
      const response = await request(app).post("/comprar").send({
        id: 1000000000
      });

      await expect(response.statusCode).toBe(500);
    });
  });
});

afterAll((done) => {
  server.close(done);
});
