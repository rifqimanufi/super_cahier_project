-- create schema
CREATE SCHEMA `super_cashier`;

-- create transaction table
CREATE TABLE IF NOT EXISTS super_cashier.transaction_table (
	trc_id INT NOT NULL,
    jumlah_item INT NOT NULL,
	harga INT NOT NULL,
    diskon VARCHAR(10),
    total_harga INT NOT NULL,
    tanggal DATE NOT NULL,
	PRIMARY KEY (trc_id)
);

-- create transaction detail table
CREATE TABLE IF NOT EXISTS super_cashier.transaction_detail_table (
	trc_id INT NOT NULL,
    item_id INT NOT NULL,
    nama_item VARCHAR(50) NOT NULL,
    jumlah_item INT NOT NULL,
	harga INT NOT NULL,
    total_harga INT NOT NULL,
    tanggal DATE NOT NULL
);

-- create data produk table
CREATE TABLE IF NOT EXISTS super_cashier.data_produk (
    item_id INT NOT NULL,
    nama_item VARCHAR(50) NOT NULL,
	harga INT NOT NULL,
	PRIMARY KEY (item_id)
);