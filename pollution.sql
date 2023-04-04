-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `pollution-db` ;

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution-db` ;
USE `pollution-db` ;

-- -----------------------------------------------------
-- Table `pollution-db`.`station`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution-db`.`station` ;

CREATE TABLE IF NOT EXISTS `pollution-db`.`station` (
  `id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `geo_point_2d` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pollution-db`.`reading`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution-db`.`reading` ;

CREATE TABLE IF NOT EXISTS `pollution-db`.`reading` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_time` DATETIME NULL,
  `station_id` INT NOT NULL,
  `nox` FLOAT(10,6) NULL,
  `no2` FLOAT(10,5) NULL,
  `no` FLOAT(10,5) NULL,
  `pm_10` FLOAT(10,5) NULL,
  `nvpm_10` FLOAT(8,5) NULL,
  `vpm_10` FLOAT(8,5) NULL,
  `nvpm_25` FLOAT(8,5) NULL,
  `pm_25` FLOAT(8,5) NULL,
  `vpm_25` FLOAT(8,5) NULL,
  `co` FLOAT(8,5) NULL,
  `o3` FLOAT(8,5) NULL,
  `so2` FLOAT(8,5) NULL,
  `temperature` FLOAT(8,5) NULL,
  `rh` FLOAT(8,5) NULL,
  `air_pressure` FLOAT(8,5) NULL,
  `date_start` DATETIME NULL,
  `date_end` DATETIME NULL,
  `current` VARCHAR(10) NULL,
  `instrument_type` VARCHAR(100) NULL,
  PRIMARY KEY (`id`, `station_id`),
  INDEX `fk_reading_station_idx` (`station_id` ASC) VISIBLE,
  CONSTRAINT `fk_reading_station`
    FOREIGN KEY (`station_id`)
    REFERENCES `pollution-db`.`station` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution-db`.`schema`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pollution-db`.`schema` ;

CREATE TABLE IF NOT EXISTS `pollution-db`.`schema` (
  `id` INT NOT NULL,
  `measure` VARCHAR(45) NULL,
  `desc` VARCHAR(45) NULL,
  `unit` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
