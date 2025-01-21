import mysql.connector
import config

async def create(nameNewDatabase):
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['mysql']['host'] ,
        user= mysqlConector['mysql']['user'],
        port =   mysqlConector['mysql']['port'],
        password= mysqlConector['mysql']['password'],
        database=nameNewDatabase
    )
   
    cursor = cnx.cursor()
    query = ''' 
    /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

# Volcado de tabla bill_fiance
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bill_fiance`;

CREATE TABLE `bill_fiance` (
  `id_finance` int NOT NULL AUTO_INCREMENT,
  `year_finace` year DEFAULT NULL,
  `month_fiance` int DEFAULT NULL,
  `income_mp` varchar(100) DEFAULT NULL,
  `electronic_ticket` double DEFAULT NULL,
  `fees` double DEFAULT NULL,
  `expences` double DEFAULT NULL,
  `office_tickets` double DEFAULT NULL,
  `cost_bill` double DEFAULT NULL,
  `gross_margin` double DEFAULT NULL,
  PRIMARY KEY (`id_finance`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla bill_media
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bill_media`;

CREATE TABLE `bill_media` (
  `id_media` int NOT NULL AUTO_INCREMENT,
  `id_bill` int DEFAULT NULL,
  `year` int DEFAULT NULL,
  `month` int DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id_media`),
  KEY `id_bill` (`id_bill`),
  CONSTRAINT `bill_media_ibfk_1` FOREIGN KEY (`id_bill`) REFERENCES `bill_fiance` (`id_finance`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla binnacle_error
# ------------------------------------------------------------

DROP TABLE IF EXISTS `binnacle_error`;

CREATE TABLE `binnacle_error` (
  `id_binnacle` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  PRIMARY KEY (`id_binnacle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla customer
# ------------------------------------------------------------

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `lastname_2` varchar(100) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `password` varchar(500) DEFAULT NULL,
  `password_firebase` varchar(500) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `create_at` date DEFAULT NULL,
  `is_reset_password` tinyint DEFAULT '1',
  `fan_id` int DEFAULT NULL,
  `ban_motive` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `is_confirm` tinyint DEFAULT '0',
  `phone_number` bigint DEFAULT NULL,
  `id_link` int DEFAULT NULL,
  `provider` enum('APPLE','EMAIL','FACEBOOK','GOOGLE') DEFAULT 'EMAIL',
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# Volcado de tabla customer_refound_requests
# ------------------------------------------------------------

DROP TABLE IF EXISTS `customer_refound_requests`;

CREATE TABLE `customer_refound_requests` (
  `id_cancelation` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `amount_discount` double DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `tickets` int DEFAULT NULL,
  `total_tickets` int DEFAULT NULL,
  `reservations` varchar(50) DEFAULT NULL,
  `is_attend` tinyint DEFAULT '0',
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_cancelation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla enclosure_chunk
# ------------------------------------------------------------

DROP TABLE IF EXISTS `enclosure_chunk`;

CREATE TABLE `enclosure_chunk` (
  `id_chunk` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `id_section` int DEFAULT NULL,
  `row_total` int DEFAULT NULL,
  `column_total` int DEFAULT NULL,
  `last_update` date DEFAULT NULL,
  `id_svg` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_chunk`),
  KEY `id_section` (`id_section`),
  CONSTRAINT `enclosure_chunk_ibfk_1` FOREIGN KEY (`id_section`) REFERENCES `enclosure_section` (`id_section`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla enclosure_row
# ------------------------------------------------------------

DROP TABLE IF EXISTS `enclosure_row`;

CREATE TABLE `enclosure_row` (
  `id_row` int NOT NULL AUTO_INCREMENT,
  `id_chunk` int DEFAULT NULL,
  `row_name` varchar(20) DEFAULT NULL,
  `num_seat` int DEFAULT NULL,
  `show` tinyint DEFAULT '1',
  `id_svg_chunk` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_row`),
  KEY `id_chunk` (`id_chunk`),
  CONSTRAINT `enclosure_row_ibfk_1` FOREIGN KEY (`id_chunk`) REFERENCES `enclosure_chunk` (`id_chunk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla enclosure_section
# ------------------------------------------------------------

DROP TABLE IF EXISTS `enclosure_section`;

CREATE TABLE `enclosure_section` (
  `id_section` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `id_enclosure` int DEFAULT NULL,
  `class_name` varchar(100) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_section`),
  KEY `id_enclosure` (`id_enclosure`),
  CONSTRAINT `enclosure_section_ibfk_1` FOREIGN KEY (`id_enclosure`) REFERENCES `settings_enclosure` (`id_enclosure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_coupons
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_coupons`;

CREATE TABLE `event_coupons` (
  `id_coupon` int NOT NULL AUTO_INCREMENT,
  `key_word` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `id_event` int DEFAULT NULL,
  `type_coupon` enum('DISCOUNT','PERCENT','COURTESY','VIP','PROMOTION','GENERAL') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `value` double DEFAULT NULL,
  `amount_coupon` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  `type_application` enum('TICKET','AMOUNT') DEFAULT NULL,
  `type_disacount` enum('CASH','PERCENT') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `available` int DEFAULT NULL COMMENT 'Total de cupones disponibles',
  PRIMARY KEY (`id_coupon`),
  KEY `id_event` (`id_event`),
  CONSTRAINT `event_coupons_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_coupons_tickets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_coupons_tickets`;

CREATE TABLE `event_coupons_tickets` (
  `id_coupon_ticket` int NOT NULL AUTO_INCREMENT,
  `id_counpon` int DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `is_available` tinyint DEFAULT '1',
  PRIMARY KEY (`id_coupon_ticket`),
  KEY `event_coupons_tickets_ibfk_1` (`id_counpon`),
  CONSTRAINT `fk_coupon` FOREIGN KEY (`id_counpon`) REFERENCES `event_coupons` (`id_coupon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_fees
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_fees`;

CREATE TABLE `event_fees` (
  `id_event_fees` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `id_fees` int DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `apply` tinyint DEFAULT '1',
  PRIMARY KEY (`id_event_fees`),
  KEY `id_event` (`id_event`),
  KEY `id_fees` (`id_fees`),
  CONSTRAINT `event_fees_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`),
  CONSTRAINT `event_fees_ibfk_2` FOREIGN KEY (`id_fees`) REFERENCES `settings_fees` (`id_fees`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_fees_reservation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_fees_reservation`;

CREATE TABLE `event_fees_reservation` (
  `id_event_fees_reservation` int NOT NULL AUTO_INCREMENT,
  `id_fees` int DEFAULT NULL,
  `id_reservation` int DEFAULT NULL,
  PRIMARY KEY (`id_event_fees_reservation`),
  KEY `id_fees` (`id_fees`),
  KEY `id_reservation` (`id_reservation`),
  CONSTRAINT `event_fees_reservation_ibfk_1` FOREIGN KEY (`id_fees`) REFERENCES `event_fees` (`id_event_fees`),
  CONSTRAINT `event_fees_reservation_ibfk_2` FOREIGN KEY (`id_reservation`) REFERENCES `event_reservations` (`id_reservation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_paid
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_paid`;

CREATE TABLE `event_paid` (
  `id_paid` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `subtotal` double DEFAULT NULL,
  `total_fee_gateway` double DEFAULT NULL,
  `total_percent` double DEFAULT NULL,
  `total_cash` double DEFAULT NULL,
  `total` double DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  PRIMARY KEY (`id_paid`),
  KEY `fk_event_pre_sale` (`id_event`),
  CONSTRAINT `fk_event_pre_sale` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_paid_binnacle
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_paid_binnacle`;

CREATE TABLE `event_paid_binnacle` (
  `id_binnacle` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `status_response` int DEFAULT NULL,
  `response_message` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id_binnacle`),
  KEY `fk_event` (`id_event`),
  CONSTRAINT `fk_event` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_pre_sale
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_pre_sale`;

CREATE TABLE `event_pre_sale` (
  `id_pre_sale` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  `id_event` int DEFAULT NULL,
  `require_code` tinyint DEFAULT '0',
  `code` varchar(100) DEFAULT NULL,
  `limit_sale` int DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  PRIMARY KEY (`id_pre_sale`),
  KEY `id_event` (`id_event`),
  CONSTRAINT `event_pre_sale_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_pre_sale_zones
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_pre_sale_zones`;

CREATE TABLE `event_pre_sale_zones` (
  `id_epsz` int NOT NULL AUTO_INCREMENT,
  `id_pre_sale` int DEFAULT NULL,
  `id_zone` int DEFAULT NULL,
  `price` double DEFAULT NULL,
  PRIMARY KEY (`id_epsz`),
  KEY `id_pre_sale` (`id_pre_sale`),
  CONSTRAINT `event_pre_sale_zones_ibfk_1` FOREIGN KEY (`id_pre_sale`) REFERENCES `event_pre_sale` (`id_pre_sale`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_reservations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_reservations`;

CREATE TABLE `event_reservations` (
  `id_reservation` int NOT NULL AUTO_INCREMENT,
  `status` enum('IN PAYMENT PROCESS','CANCEL','COURTESY','PAID','RESERVED') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'RESERVED',
  `amount` int DEFAULT NULL,
  `total_tickets` double DEFAULT NULL,
  `total_fees` double DEFAULT NULL,
  `real_fees_payment_gateway` double DEFAULT NULL,
  `fee_payment_gateway` float DEFAULT '0',
  `sub_total` double DEFAULT NULL,
  `iva` double DEFAULT NULL,
  `total` double DEFAULT NULL,
  `id_event` int DEFAULT NULL,
  `fan_id` int DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `credit_card` int DEFAULT NULL,
  `mpp_transaction` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `type_payment` enum('taquilla','cash','card','paypal') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `type_ticket` enum('venta general','bono gallo','palco','taquilla','cortesia') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `inbropi_fees` DOUBLE,
  `id_presale` int DEFAULT NULL,
  PRIMARY KEY (`id_reservation`),
  KEY `fk_event_id` (`id_event`),
  CONSTRAINT `fk_event_id` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_reservations_tickets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_reservations_tickets`;

CREATE TABLE `event_reservations_tickets` (
  `id_ert` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `id_reservation` int DEFAULT NULL,
  `id_row` int DEFAULT NULL,
  `id_fan` int DEFAULT NULL,
  `id_section` int DEFAULT NULL,
  `id_chunk` int DEFAULT NULL,
  `id_coupon` int DEFAULT NULL,
  `seat_num` int DEFAULT NULL,
  `row_name` varchar(15) DEFAULT NULL,
  `status` enum('RESERVED','CANCEL') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'RESERVED',
  `price` double DEFAULT NULL,
  `coupon_discount` double DEFAULT NULL,
  `has_printed` tinyint DEFAULT '0',
  `is_check` tinyint DEFAULT (false),
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_ert`),
  KEY `event_reservations_tickets_ibfk_1` (`id_reservation`),
  KEY `fk_customer` (`id_fan`),
  KEY `fk_event_info` (`id_event`),
  CONSTRAINT `fk_customer` FOREIGN KEY (`id_fan`) REFERENCES `customer` (`id_user`),
  CONSTRAINT `fk_event_info` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_ticket
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_ticket`;

CREATE TABLE `event_ticket` (
  `id_ticket_event` int NOT NULL AUTO_INCREMENT,
  `id_ticket` int DEFAULT NULL,
  `price` double DEFAULT NULL,
  `id_event` int DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  PRIMARY KEY (`id_ticket_event`),
  KEY `fk_event_ticket` (`id_event`),
  CONSTRAINT `fk_event_ticket` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla event_types
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event_types`;

CREATE TABLE `event_types` (
  `id_type` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(150) DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  `crete_at` date DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla events
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events`;

CREATE TABLE `events` (
  `id_event` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `date_event` date DEFAULT NULL,
  `time_event` time DEFAULT NULL,
  `id_clasification` int DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  `is_public` tinyint DEFAULT '0',
  `id_enclosure` int DEFAULT NULL,
  `situation` enum('NO PUBLICADO','PUBLICADO','POSPUESTO','CANCELADO') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'NO PUBLICADO',
  `status` enum('ACTIVO','CANCELADO','TERMINADO','GENERADO','PAGADO','EN PROCESO DE PAGO') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'GENERADO',
  `share_path` varchar(500) DEFAULT NULL,
  `post_sale` varchar(2000) DEFAULT NULL,
  `id_type_event` int DEFAULT NULL,
  `paid_date` date DEFAULT NULL,
  `id_referece` varchar(100) DEFAULT NULL,
  `gateway_name` enum('MERCADO PAGO','PAYPAL') DEFAULT NULL,
  `inbropi_fees` double DEFAULT NULL,
  `time_zone_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_event`),
  KEY `fk_clasification` (`id_clasification`),
  KEY `fk_enclosure` (`id_enclosure`),
  KEY `fk_event_type` (`id_type_event`),
  CONSTRAINT `fk_clasification` FOREIGN KEY (`id_clasification`) REFERENCES `settings_event_classification` (`id_category`),
  CONSTRAINT `fk_enclosure` FOREIGN KEY (`id_enclosure`) REFERENCES `settings_enclosure` (`id_enclosure`),
  CONSTRAINT `fk_event_type` FOREIGN KEY (`id_type_event`) REFERENCES `event_types` (`id_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
# Volcado de tabla events_bill
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_bill`;

CREATE TABLE `events_bill` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `id_concept` int DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_event` (`id_event`),
  KEY `id_concept` (`id_concept`),
  CONSTRAINT `events_bill_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`),
  CONSTRAINT `events_bill_ibfk_2` FOREIGN KEY (`id_concept`) REFERENCES `settings_bill_concept` (`id_concept`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla media
# ------------------------------------------------------------

DROP TABLE IF EXISTS `media`;

CREATE TABLE `media` (
  `id_media` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `id_event` int DEFAULT NULL,
  `createAt` date DEFAULT NULL,
  `id_enclosure` int DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  `id_customer` int DEFAULT NULL,
  PRIMARY KEY (`id_media`),
  KEY `fk_ticket` (`id_customer`),
  KEY `fk_idUser` (`id_user`),
  KEY `id_event` (`id_event`),
  CONSTRAINT `fk_idUser` FOREIGN KEY (`id_user`) REFERENCES `settings_users` (`id_user`),
  CONSTRAINT `fk_ticket` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`id_user`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `media_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla paid_event
# ------------------------------------------------------------

DROP TABLE IF EXISTS `paid_event`;

CREATE TABLE `paid_event` (
  `id_paid` int NOT NULL AUTO_INCREMENT,
  `id_event` int DEFAULT NULL,
  `subtotad` double DEFAULT NULL,
  `total_fee_gateway` double DEFAULT NULL,
  `total` double DEFAULT NULL,
  PRIMARY KEY (`id_paid`),
  KEY `id_event` (`id_event`),
  CONSTRAINT `paid_event_ibfk_1` FOREIGN KEY (`id_event`) REFERENCES `events` (`id_event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla payment_binnacle
# ------------------------------------------------------------

DROP TABLE IF EXISTS `payment_binnacle`;

CREATE TABLE `payment_binnacle` (
  `id_binnacle` int NOT NULL AUTO_INCREMENT,
  `id_reference` bigint DEFAULT NULL,
  `status` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_binnacle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_actions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_actions`;

CREATE TABLE `settings_actions` (
  `id_action` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  PRIMARY KEY (`id_action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_bill_concept
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_bill_concept`;

CREATE TABLE `settings_bill_concept` (
  `id_concept` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  PRIMARY KEY (`id_concept`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_enclosure
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_enclosure`;

CREATE TABLE `settings_enclosure` (
  `id_enclosure` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `enclosure_address` varchar(250) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  PRIMARY KEY (`id_enclosure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_event_classification
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_event_classification`;

CREATE TABLE `settings_event_classification` (
  `id_category` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `create_at` date DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_category`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `settings_event_classification_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `settings_users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_fees
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_fees`;

CREATE TABLE `settings_fees` (
  `id_fees` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `value` double DEFAULT NULL,
  `type_fees` enum('PERCENT','CASH') DEFAULT NULL,
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `subtitle` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `type_application` enum('TICKET','AMOUNT') DEFAULT NULL,
  `forced` tinyint DEFAULT '1',
  `is_active` tinyint DEFAULT '1',
  `id_group` int DEFAULT '1',
  PRIMARY KEY (`id_fees`),
  KEY `id_group` (`id_group`),
  CONSTRAINT `settings_fees_ibfk_1` FOREIGN KEY (`id_group`) REFERENCES `settings_fees_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_fees_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_fees_group`;

CREATE TABLE `settings_fees_group` (
  `id_group` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  PRIMARY KEY (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_gateway
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_gateway`;

CREATE TABLE `settings_gateway` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  `value_percent` float DEFAULT NULL,
  `value_cash` float DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `create_at` date DEFAULT NULL,
  `update_at` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_modules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_modules`;

CREATE TABLE `settings_modules` (
  `id_module` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `createAt` date DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_module`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `settings_modules_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `settings_users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_permitions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_permitions`;

CREATE TABLE `settings_permitions` (
  `id_permition` int NOT NULL AUTO_INCREMENT,
  `id_module` int DEFAULT NULL,
  `id_submodule` int DEFAULT NULL,
  `id_action` int DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_permition`),
  KEY `id_action` (`id_action`),
  CONSTRAINT `settings_permitions_ibfk_1` FOREIGN KEY (`id_action`) REFERENCES `settings_actions` (`id_action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_role_permitions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_role_permitions`;

CREATE TABLE `settings_role_permitions` (
  `id_link` int NOT NULL AUTO_INCREMENT,
  `id_rol` int DEFAULT NULL,
  `id_permition` int DEFAULT NULL,
  PRIMARY KEY (`id_link`),
  KEY `id_rol` (`id_rol`),
  KEY `id_permition` (`id_permition`),
  CONSTRAINT `settings_role_permitions_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `settings_roles` (`id_rol`),
  CONSTRAINT `settings_role_permitions_ibfk_2` FOREIGN KEY (`id_permition`) REFERENCES `settings_permitions` (`id_permition`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_roles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_roles`;

CREATE TABLE `settings_roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `createAt` date DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_rol`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `settings_roles_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `settings_users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_stage
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_stage`;

CREATE TABLE `settings_stage` (
  `id_setting` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `value` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_setting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_submodules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_submodules`;

CREATE TABLE `settings_submodules` (
  `id_submodule` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `createAt` date DEFAULT NULL,
  `id_module` int DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_submodule`),
  KEY `id_module` (`id_module`),
  CONSTRAINT `settings_submodules_ibfk_1` FOREIGN KEY (`id_module`) REFERENCES `settings_modules` (`id_module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_tickets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_tickets`;

CREATE TABLE `settings_tickets` (
  `id_ticket` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL,
  `id_enclosure` int DEFAULT NULL,
  `available_seats` int DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `id_section` int DEFAULT NULL,
  PRIMARY KEY (`id_ticket`),
  KEY `id_section` (`id_section`),
  CONSTRAINT `settings_tickets_ibfk_1` FOREIGN KEY (`id_section`) REFERENCES `enclosure_section` (`id_section`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Volcado de tabla settings_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings_users`;

CREATE TABLE `settings_users` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `lastname_2` varchar(100) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `password` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `phone_number` bigint DEFAULT NULL,
  `id_rol` int DEFAULT NULL,
  `isActive` tinyint DEFAULT '1',
  `createAt` date DEFAULT NULL,
  `is_reset_password` tinyint DEFAULT '0',
  `user_type` enum('ADMIN','PUBLIC') DEFAULT 'ADMIN',
  `fan_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

    '''
    cursor.execute(query)

    cursor.close()
    cnx.close() 
    return 'success'
