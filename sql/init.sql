--来源网站
create table website(
  id SERIAL PRIMARY KEY ,
  name varchar(20),
  website_domain varchar(50),
  status INTEGER DEFAULT 1
);

--股票基本信息表
create table stock(
  id SERIAL PRIMARY KEY ,
  code char(6),
  name varchar(8),
  bps FLOAT , --每股净资产
  eps FLOAT , --每股收益
  net_income FLOAT , --净利润
  ngpr FLOAT , --净利润增长率
  income FLOAT , --营收
  sps FLOAT , --每股现金流
  fps FLOAT , --每股公积金
  udpps FLOAT , --每股未分配利润
  total_stock_issue INTEGER , --总股本
  liqui INTEGER --流通股本
);

--板块基本信息
create table category(
  id SERIAL PRIMARY KEY ,
  code char(6),
  name varchar(20),
  cate_type integer, --0:行业，1--概念
  url VARCHAR (100)
);

--股票板块对应关系
create table stock_category_mapping(
  id SERIAL PRIMARY KEY ,
  stock_id integer REFERENCES stock(id),
  category_id integer REFERENCES category(id)
);

--TOP15行业和概念板块
create table top_category_daily(
  id SERIAL PRIMARY KEY ,
  category_id INTEGER  REFERENCES category(id),
  ranking INTEGER,
  net_inflow FLOAT,
  rise int ,
  fall int ,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--机构表
create table shareholder(
  id SERIAL PRIMARY KEY ,
  sharehoder_name varchar(255),
  sharehoder_type varchar(100)
);

--股东人数变化统计表
create table shareholder_report(
  id SERIAL PRIMARY KEY ,
  stock_id INTEGER REFERENCES stock(id),
  report_date TIMESTAMP ,
  total_shareholder INTEGER ,
  shareholder_chain DECIMAL (5,4), --股东数环比
  avg_tradable_share INTEGER ,
  avg_tradable_share_chain DECIMAL (5,4) --人均流通股环比
);

--个股每日交易明细
create table stock_detail_daily(
  id SERIAL PRIMARY KEY ,
  stock_id INTEGER REFERENCES stock(id),
  detail_date TIMESTAMP DEFAULT now(),
  open_price DECIMAL (6,2),
  close_price DECIMAL (6,2),
  highest_price DECIMAL (6,2),
  lowest_price DECIMAL (6,2),
  trading_volume INTEGER , --成交量
  turnover bigint , --交易额
  market_value bigint , --市值
  circulated_stock_value bigint , --流通市值
  amplitude DECIMAL (6,4) , --振幅
  trading_volume_rate DECIMAL (6,4), --换手率
  pb_ratio DECIMAL (6,2), --市净率
  pe_ratio DECIMAL (6,2), --动态市盈率
  large_in bigint ,--大单流入
  mid_in bigint ,--中单流入
  small_in bigint ,--小单流入
  large_out bigint , --大单流出
  mid_out bigint , --中单流出
  small_out bigint,  --小单流出
  website INTEGER REFERENCES website(id)
);