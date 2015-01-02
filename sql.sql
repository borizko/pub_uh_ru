CREATE TABLE IF NOT EXISTS `articles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `module` VARCHAR(45) NOT NULL,
  `section` VARCHAR(255) NULL,
  `name` VARCHAR(255) NOT NULL,
  `text` TEXT NULL,
  `url` VARCHAR(255) NULL,
  `used` ENUM('0','1') NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `images_article` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `articles_id` INT UNSIGNED NOT NULL,
  `path` VARCHAR(300) NULL,
  `url` VARCHAR(300) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_images_articles_idx` (`articles_id` ASC),
  CONSTRAINT `fk_images_articles`
    FOREIGN KEY (`articles_id`)
    REFERENCES `articles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `temp_table` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `module` VARCHAR(45) NOT NULL,
  `section` VARCHAR(255) NULL,
  `articles_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_temp_table_articles1_idx` (`articles_id` ASC),
  CONSTRAINT `fk_temp_table_articles1`
    FOREIGN KEY (`articles_id`)
    REFERENCES `articles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `current_page_module` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `module` VARCHAR(45) NOT NULL,
  `section` VARCHAR(255) NULL,
  `page` MEDIUMINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

DELETE FROM temp_table;
DELETE FROM images_article;
DELETE FROM current_page_module;
DELETE FROM articles;