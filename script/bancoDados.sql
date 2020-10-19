CREATE DATABASE jbasso;
CREATE schema soja;

CREATE TABLE soja.producaosoja(
	datacotacao DATE,
	regioesimea VARCHAR(50),
	percentual DECIMAL(7,4)
);

SELECT count(*) from soja.producaoSoja
delete from soja.producaoSoja