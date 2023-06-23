

-- update product

UPDATE Product
SET quantity = 25
WHERE product_id IN (1, 5);

-- delete products that store in one of warehouse from product

DELETE FROM Product
WHERE warehouse_id = 2;


-- Create an index by product name.

CREATE INDEX idx_product_name ON Product (product_name);
