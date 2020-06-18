-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 17-06-2020 a las 21:05:04
-- Versión del servidor: 5.7.25-0ubuntu0.18.04.2
-- Versión de PHP: 7.2.28-3+ubuntu18.04.1+deb.sury.org+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `External-Api`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Token`
--

CREATE TABLE `Token` (
  `Id` int(11) NOT NULL,
  `User_Id` int(11) NOT NULL,
  `Token` text NOT NULL,
  `Time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `IsActive` int(1) NOT NULL DEFAULT '1',
  `Toke_Generated` varchar(50) NOT NULL,
  `Token_Expiration` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `User`
--

CREATE TABLE `User` (
  `Id` int(11) NOT NULL,
  `User` varchar(50) DEFAULT NULL,
  `grant_type` varchar(30) DEFAULT NULL,
  `client_id` varchar(50) DEFAULT NULL,
  `client_secret` varchar(100) DEFAULT NULL,
  `Endpoint_Id` varchar(100) DEFAULT 'undefined',
  `Environment` int(11) DEFAULT '0',
  `Intervalo` int(11) DEFAULT '10',
  `Notification` varchar(11) NOT NULL DEFAULT '0',
  `CodeUser` int(11) DEFAULT NULL,
  `Status` int(11) DEFAULT NULL,
  `RegistrationDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Token`
--
ALTER TABLE `Token`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Token`
--
ALTER TABLE `Token`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `User`
--
ALTER TABLE `User`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
