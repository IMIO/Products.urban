--
-- bestaddress database creation script : can be run with command 'psql -f bestaddress.sql'
--

-- Started on 2010-12-07 08:30:35 CET

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

CREATE ROLE bestaddressreader LOGIN
  ENCRYPTED PASSWORD 'md5e4bca05abeb22327b8e69201da25f865'
  NOSUPERUSER NOINHERIT NOCREATEDB NOCREATEROLE;

--
-- TOC entry 1744 (class 1262 OID 37714)
-- Name: bestaddress; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE bestaddress WITH TEMPLATE = template0 ENCODING = 'UTF8';


ALTER DATABASE bestaddress OWNER TO admin;

\connect bestaddress

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1467 (class 1259 OID 37715)
-- Dependencies: 6
-- Name: addresses; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE addresses (
    id integer NOT NULL,
    key integer NOT NULL,
    street character varying(100),
    regional_road character varying(20),
    zip character varying(4),
    entity character varying(50),
    commune character varying(50),
    national_code character varying(5),
    begin_date date NOT NULL,
    end_date date,
    modification character varying(100)
);


ALTER TABLE public.addresses OWNER TO admin;

--
-- TOC entry 1468 (class 1259 OID 37718)
-- Dependencies: 6 1467
-- Name: addresses_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE addresses_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.addresses_id_seq OWNER TO admin;

--
-- TOC entry 1748 (class 0 OID 0)
-- Dependencies: 1468
-- Name: addresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE addresses_id_seq OWNED BY addresses.id;


--
-- TOC entry 1469 (class 1259 OID 37723)
-- Dependencies: 1546 6
-- Name: urban_addresses; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW urban_addresses AS
    SELECT addresses.id, addresses.key, addresses.street, addresses.regional_road, addresses.zip, addresses.entity, split_part(addresses.entity,'(',1) as short_entity, addresses.commune, addresses.national_code, addresses.begin_date, addresses.end_date, addresses.modification FROM addresses WHERE (((addresses.street IS NOT NULL) AND ((addresses.end_date IS NULL) OR ((addresses.modification)::text !~~ 'Doublon%'::text))) AND (addresses.commune IS NOT NULL));


ALTER TABLE public.urban_addresses OWNER TO admin;

--
-- TOC entry 1470 (class 1259 OID 37727)
-- Dependencies: 1547 6
-- Name: urban_addresses_unkept; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW urban_addresses_unkept AS
    SELECT addresses.id, addresses.key, addresses.street, addresses.regional_road, addresses.zip, addresses.entity, addresses.commune, addresses.national_code, addresses.begin_date, addresses.end_date, addresses.modification FROM addresses WHERE (NOT (addresses.id IN (SELECT v.id FROM urban_addresses v)));


ALTER TABLE public.urban_addresses_unkept OWNER TO admin;

--
-- TOC entry 1739 (class 2604 OID 37720)
-- Dependencies: 1468 1467
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE addresses ALTER COLUMN id SET DEFAULT nextval('addresses_id_seq'::regclass);


--
-- TOC entry 1741 (class 2606 OID 37722)
-- Dependencies: 1467 1467
-- Name: Primary key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY addresses
    ADD CONSTRAINT "Primary key" PRIMARY KEY (id);


--
-- TOC entry 1746 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- TOC entry 1747 (class 0 OID 0)
-- Dependencies: 1467
-- Name: addresses; Type: ACL; Schema: public; Owner: admin
--

REVOKE ALL ON TABLE addresses FROM PUBLIC;
REVOKE ALL ON TABLE addresses FROM admin;
GRANT ALL ON TABLE addresses TO admin;
GRANT SELECT ON TABLE addresses TO bestaddressreader;


--
-- TOC entry 1749 (class 0 OID 0)
-- Dependencies: 1469
-- Name: urban_addresses; Type: ACL; Schema: public; Owner: admin
--

REVOKE ALL ON TABLE urban_addresses FROM PUBLIC;
REVOKE ALL ON TABLE urban_addresses FROM admin;
GRANT ALL ON TABLE urban_addresses TO admin;
GRANT SELECT ON TABLE urban_addresses TO bestaddressreader;


-- Completed on 2010-12-07 08:30:35 CET

--
-- PostgreSQL database dump complete
--

