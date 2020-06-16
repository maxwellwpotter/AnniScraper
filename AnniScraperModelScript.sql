-- MySQL Script generated by MySQL Workbench
-- Sat Jun 13 22:30:29 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`matches`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`matches` ;

CREATE TABLE IF NOT EXISTS `mydb`.`matches` (
  `matchID` DATETIME(3) NOT NULL COMMENT 'Time of first snapshot',
  `map` VARCHAR(45) NOT NULL,
  `joinPhase` TINYINT NOT NULL,
  `joinTime` TIME NOT NULL,
  `bluePlacing` TINYINT NULL,
  `greenPlacing` TINYINT NULL,
  `redPlacing` TINYINT NULL,
  `yellowPlacing` TINYINT NULL,
  PRIMARY KEY (`matchID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`snapshots`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`snapshots` ;

CREATE TABLE IF NOT EXISTS `mydb`.`snapshots` (
  `matchID` DATETIME(3) NOT NULL,
  `shotTime` DATETIME(3) NOT NULL,
  `blueHealth` INT NOT NULL,
  `greenHealth` INT NOT NULL,
  `redHealth` INT NOT NULL,
  `yellowHealth` INT NOT NULL,
  `nexusDamager` VARCHAR(45) NULL,
  `damagingTeam` VARCHAR(6) NULL,
  `damagedTeam` VARCHAR(6) NULL,
  `bossKilled` VARCHAR(45) NULL,
  `bossKillingTeam` VARCHAR(6) NULL COMMENT 'Null if boss was not killed\n',
  `phase` TINYINT NULL,
  `phaseTimeRemaining` TIME NULL,
  PRIMARY KEY (`matchID`, `shotTime`),
  INDEX `fk_snapshots_matches_idx` (`matchID` ASC) VISIBLE,
  CONSTRAINT `fk_snapshots_matches`
    FOREIGN KEY (`matchID`)
    REFERENCES `mydb`.`matches` (`matchID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kills` ;

CREATE TABLE IF NOT EXISTS `mydb`.`kills` (
  `snapshots_matchID` DATETIME(3) NOT NULL,
  `snapshots_shotTime` DATETIME(3) NOT NULL,
  `killIndexInShot` INT NOT NULL,
  `killer` VARCHAR(45) NOT NULL,
  `killerClass` VARCHAR(3) NOT NULL,
  `killerTeam` VARCHAR(6) NOT NULL,
  `meleeKill` TINYINT NOT NULL,
  `killed` VARCHAR(45) NOT NULL,
  `killedClass` VARCHAR(3) NOT NULL,
  `killedTeam` VARCHAR(45) NOT NULL,
  `isAttacking` TINYINT(1) NULL COMMENT 'True if the kill was while attacking\nFalse if the kill was while defending\nNull if the kill was neither\n',
  `attackedOrDefendedNexus` VARCHAR(6) NULL,
  PRIMARY KEY (`snapshots_matchID`, `snapshots_shotTime`, `killIndexInShot`, `killer`, `killed`),
  CONSTRAINT `fk_kills_snapshots1`
    FOREIGN KEY (`snapshots_matchID` , `snapshots_shotTime`)
    REFERENCES `mydb`.`snapshots` (`matchID` , `shotTime`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
