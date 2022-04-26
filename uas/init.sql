DROP TABLE IF EXISTS users;
CREATE TABLE users 
  (userId SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL, 
  password VARCHAR(255) NOT NULL,
  email TEXT,
  name VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  phone VARCHAR(25));



DROP TABLE IF EXISTS categories;
CREATE TABLE categories
  (categoryId INTEGER PRIMARY KEY,
  name TEXT
  );
  
DROP TABLE IF EXISTS products;
CREATE TABLE products
  (productId INTEGER PRIMARY KEY,
  productBrand TEXT,
  productName TEXT,
  price INTEGER,
  description TEXT,
  image TEXT,
  stock INTEGER,
  categoryId INTEGER,
  FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
  userId INTEGER,
  FOREIGN KEY(userId) REFERENCES users(userId)
  );

DROP TABLE IF EXISTS kart;
CREATE TABLE kart
  (userId INTEGER,
  productId INTEGER,
  FOREIGN KEY(userId) REFERENCES users(userId),
  FOREIGN KEY(productId) REFERENCES products(productId)
  );

INSERT INTO users (username, name, password) VALUES ('admin', 'Administrator', 'admin');