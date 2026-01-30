--
-- PostgreSQL database dump
--

\restrict 6N1gfbETXMlbXbp5vnhqyja28IXXRcJlY8xyIrdicRKNiHx7Nukx5LY6PHCRWxl

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.1 (Ubuntu 18.1-1.pgdg25.10+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO guest;

--
-- Name: authors; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.authors (
    id integer NOT NULL,
    firstname character varying(128) NOT NULL,
    lastname character varying(128) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(15),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    modified_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.authors OWNER TO guest;

--
-- Name: authors_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.authors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.authors_id_seq OWNER TO guest;

--
-- Name: authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.authors_id_seq OWNED BY public.authors.id;


--
-- Name: books; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying(128) NOT NULL,
    isbn character varying(255) NOT NULL,
    page_count integer NOT NULL,
    author_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    modified_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.books OWNER TO guest;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_id_seq OWNER TO guest;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.users (
    id integer NOT NULL,
    firstname character varying(128) NOT NULL,
    lastname character varying(128) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(15),
    password character varying(128),
    lastlogin timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    modified_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO guest;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO guest;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: authors id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.authors ALTER COLUMN id SET DEFAULT nextval('public.authors_id_seq'::regclass);


--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.alembic_version (version_num) FROM stdin;
84f8ba08e237
\.


--
-- Data for Name: authors; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.authors (id, firstname, lastname, email, phone, created_at, modified_at) FROM stdin;
1	JK	Rowing	jk@rowing.com	+49123456789	2026-01-30 14:45:21.230749+00	2026-01-30 14:45:21.230749+00
\.


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.books (id, title, isbn, page_count, author_id, created_at, modified_at) FROM stdin;
1	Harry Porter	978-0-596-52068-7	123	1	2026-01-30 14:46:48.081686+00	2026-01-30 14:46:48.081686+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.users (id, firstname, lastname, email, phone, password, lastlogin, created_at, modified_at) FROM stdin;
1	Kok How	Teh	khteh@email.com	\N	$2b$10$3zixeio4.1.OU.5OgdXLvuCbwk40ZyyWxD7xtlL1Joil04dSC/lHK	\N	2026-01-30 14:44:45.219441+00	2026-01-30 14:44:45.219441+00
\.


--
-- Name: authors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.authors_id_seq', 1, true);


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.books_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: authors authors_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (id);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_authors_email; Type: INDEX; Schema: public; Owner: guest
--

CREATE UNIQUE INDEX ix_authors_email ON public.authors USING btree (email);


--
-- Name: ix_authors_phone; Type: INDEX; Schema: public; Owner: guest
--

CREATE UNIQUE INDEX ix_authors_phone ON public.authors USING btree (phone);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: guest
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_phone; Type: INDEX; Schema: public; Owner: guest
--

CREATE UNIQUE INDEX ix_users_phone ON public.users USING btree (phone);


--
-- Name: books books_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 6N1gfbETXMlbXbp5vnhqyja28IXXRcJlY8xyIrdicRKNiHx7Nukx5LY6PHCRWxl

