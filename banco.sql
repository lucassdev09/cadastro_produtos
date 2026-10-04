create table produtos (
    id INT NOT NULL AUTO_INCREMENT,
    codigo INT,
    descricao VARCHAR(50),
    preco DOUBLE,
    categoria VARCHAR(20),
    PRIMARY KEY (id)
);

# inserindo registros na tabela

INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (123, "impressora", 500.00, "informatica");