
-- create table product

CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit_weight DECIMAL(10, 2) NOT NULL,
    availability BOOLEAN NOT NULL,
    availability_date DATE,
    price DECIMAL(10, 2) NOT NULL,
    product_category VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    manufacturer_code VARCHAR(255) NOT NULL,
    dimensions VARCHAR(255)
);

-- create table warehouse 

CREATE TABLE Warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR(255) NOT NULL,
    area DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    warehouse_type VARCHAR(255) NOT NULL
);

-- binding warehouse table to product

ALTER TABLE Product
ADD COLUMN warehouse_id INT,
ADD CONSTRAINT fk_warehouse
    FOREIGN KEY (warehouse_id)
    REFERENCES Warehouse(warehouse_id);
    
   
--  insert rows in warehouse

INSERT INTO Warehouse (warehouse_id, warehouse_name, area, location, warehouse_type)
VALUES
    (1, 'Warehouse firstwh', 1000.50, 'Odesa', 'open'),
    (2, 'Warehouse secondewh', 750.25, 'Kiyv', 'closed'),
    (3, 'Warehouse thirdwh', 1200.75, 'Lviv', 'closed');
    
   
 --  insert rows in product
  
INSERT INTO Product (product_id, product_name, quantity, unit_weight, availability, availability_date, price, product_category, brand, manufacturer_code, warehouse_id)
VALUES
    (1, 'Product 1', 5, 1.25, true, '2023-06-20', 10.99, 'Category A', 'Brand X', 'M-001', 1),
    (2, 'Product 2', 3, 2.50, true, '2023-06-21', 19.99, 'Category B', 'Brand Y', 'M-002', 1),
    (3, 'Product 3', 8, 0.75, true, '2023-06-22', 5.99, 'Category A', 'Brand Z', 'M-003', 2),
    (4, 'Product 4', 2, 1.00, false, '2023-06-25', 14.99, 'Category C', 'Brand X', 'M-004', 2),
    (5, 'Product 5', 10, 1.50, true, '2023-06-23', 9.99, 'Category B', 'Brand Y', 'M-005', 3),
    (6, 'Product 6', 4, 0.50, true, '2023-06-24', 7.99, 'Category A', 'Brand Z', 'M-006', 3),
    (7, 'Product 7', 6, 1.75, true, '2023-06-25', 11.99, 'Category C', 'Brand X', 'M-007', 1),
    (8, 'Product 8', 1, 2.00, false, '2023-06-25', 16.99, 'Category A', 'Brand Y', 'M-008', 2),
    (9, 'Product 9', 9, 1.25, true, '2023-06-26', 13.99, 'Category B', 'Brand Z', 'M-009', 2),
    (10, 'Product 10', 7, 1.50, true, '2023-06-27', 8.99, 'Category C', 'Brand X', 'M-010', 3);
   
   
-- update product

UPDATE Product
SET quantity = 25
WHERE product_id IN (1, 5);

-- delete products that store in one of warehouse from product

DELETE FROM Product
WHERE warehouse_id = 2;


-- Create an index by product name.

CREATE INDEX idx_product_name ON Product (product_name);


   
   
   
   
