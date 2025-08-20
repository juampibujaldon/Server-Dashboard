db = db.getSiblingDB('admin');

db.createUser({
  user: process.env.MONGO_APP_USER,
  pwd: process.env.MONGO_APP_PASSWORD,
  roles: [
    { role: 'readWrite', db: 'DEV_MONITOREAR' },
    { role: 'readWrite', db: 'TEST_MONITOREAR' },
    { role: 'dbAdmin', db: 'TEST_MONITOREAR' },
    { role: 'readWrite', db: 'PROD_MONITOREAR' }
  ],
});

db.getSiblingDB('DEV_MONITOREAR').createCollection('metricas');
db.getSiblingDB('TEST_MONITOREAR').createCollection('metricas');
db.getSiblingDB('PROD_MONITOREAR').createCollection('metricas');