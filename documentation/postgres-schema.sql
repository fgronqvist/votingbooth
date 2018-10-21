--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-1.pgdg14.04+1)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-1.pgdg16.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_modified timestamp with time zone,
    firstname character varying(256) NOT NULL,
    lastname character varying(256) NOT NULL,
    email character varying(256) NOT NULL,
    password character varying(256) NOT NULL
);


--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.account_id_seq OWNED BY public.account.id;


--
-- Name: account_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account_role (
    id integer NOT NULL,
    account_id integer NOT NULL,
    name character varying(256) NOT NULL
);


--
-- Name: account_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.account_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: account_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.account_role_id_seq OWNED BY public.account_role.id;


--
-- Name: poll; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.poll (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_modified timestamp with time zone,
    name character varying(256) NOT NULL,
    owner_id integer NOT NULL,
    date_open timestamp with time zone,
    date_close timestamp with time zone,
    anynomous boolean
);


--
-- Name: poll_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.poll_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: poll_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.poll_id_seq OWNED BY public.poll.id;


--
-- Name: user_voted; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_voted (
    id integer NOT NULL,
    poll_id integer NOT NULL,
    account_id integer NOT NULL,
    date_created timestamp with time zone
);


--
-- Name: user_voted_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_voted_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_voted_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_voted_id_seq OWNED BY public.user_voted.id;


--
-- Name: vote; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vote (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_modified timestamp with time zone,
    poll_id integer NOT NULL,
    vote_option_id integer NOT NULL
);


--
-- Name: vote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vote_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vote_id_seq OWNED BY public.vote.id;


--
-- Name: vote_option; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vote_option (
    id integer NOT NULL,
    poll_id integer NOT NULL,
    ordernum integer NOT NULL,
    name character varying(256) NOT NULL
);


--
-- Name: vote_option_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vote_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vote_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vote_option_id_seq OWNED BY public.vote_option.id;


--
-- Name: account id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account ALTER COLUMN id SET DEFAULT nextval('public.account_id_seq'::regclass);


--
-- Name: account_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_role ALTER COLUMN id SET DEFAULT nextval('public.account_role_id_seq'::regclass);


--
-- Name: poll id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.poll ALTER COLUMN id SET DEFAULT nextval('public.poll_id_seq'::regclass);


--
-- Name: user_voted id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_voted ALTER COLUMN id SET DEFAULT nextval('public.user_voted_id_seq'::regclass);


--
-- Name: vote id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote ALTER COLUMN id SET DEFAULT nextval('public.vote_id_seq'::regclass);


--
-- Name: vote_option id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote_option ALTER COLUMN id SET DEFAULT nextval('public.vote_option_id_seq'::regclass);


--
-- Name: account account_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_email_key UNIQUE (email);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: account_role account_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_role
    ADD CONSTRAINT account_role_pkey PRIMARY KEY (id);


--
-- Name: poll poll_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.poll
    ADD CONSTRAINT poll_pkey PRIMARY KEY (id);


--
-- Name: user_voted user_voted_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_voted
    ADD CONSTRAINT user_voted_pkey PRIMARY KEY (id);


--
-- Name: vote_option vote_option_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote_option
    ADD CONSTRAINT vote_option_pkey PRIMARY KEY (id);


--
-- Name: vote vote_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote
    ADD CONSTRAINT vote_pkey PRIMARY KEY (id);


--
-- Name: account_role account_role_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_role
    ADD CONSTRAINT account_role_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id);


--
-- Name: poll poll_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.poll
    ADD CONSTRAINT poll_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.account(id);


--
-- Name: user_voted user_voted_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_voted
    ADD CONSTRAINT user_voted_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id);


--
-- Name: user_voted user_voted_poll_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_voted
    ADD CONSTRAINT user_voted_poll_id_fkey FOREIGN KEY (poll_id) REFERENCES public.poll(id);


--
-- Name: vote_option vote_option_poll_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote_option
    ADD CONSTRAINT vote_option_poll_id_fkey FOREIGN KEY (poll_id) REFERENCES public.poll(id);


--
-- Name: vote vote_poll_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote
    ADD CONSTRAINT vote_poll_id_fkey FOREIGN KEY (poll_id) REFERENCES public.poll(id);


--
-- Name: vote vote_vote_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vote
    ADD CONSTRAINT vote_vote_option_id_fkey FOREIGN KEY (vote_option_id) REFERENCES public.vote_option(id);


--
-- PostgreSQL database dump complete
--

