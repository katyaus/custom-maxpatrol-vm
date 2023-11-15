--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: os; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.os (
    os_id integer NOT NULL,
    os_type character varying(100),
    os_vers character varying(100),
    cpu_arch character varying(100),
    kernel_vers character varying(100),
    addr_host character varying(100)
);


ALTER TABLE public.os OWNER TO postgres;

--
-- Name: operation_system_os_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.os ALTER COLUMN os_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.operation_system_os_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: os; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.os (os_id, os_type, os_vers, cpu_arch, kernel_vers, addr_host) FROM stdin;
14	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
15	GNU/Linux	Ubuntu 20.04.6 LTS	x86_64	5.15.0-88-generic	192.168.1.77
16	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
17	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
18	GNU/Linux	Ubuntu 20.04.6 LTS	x86_64	5.15.0-88-generic	192.168.1.77
19	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
20	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
21	GNU/Linux	Kali GNU/Linux Rolling	x86_64	6.3.0-kali1-amd64	192.168.1.67
\.


--
-- Name: operation_system_os_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operation_system_os_id_seq', 21, true);


--
-- Name: os operation_system_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.os
    ADD CONSTRAINT operation_system_pkey PRIMARY KEY (os_id);


--
-- PostgreSQL database dump complete
--

