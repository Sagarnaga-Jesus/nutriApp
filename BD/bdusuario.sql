/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `bdnutriapp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci */;
USE `bdnutriapp`;

CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `altura` float DEFAULT NULL,
  `actividad` varchar(40) DEFAULT NULL,
  `sexo` varchar(25) DEFAULT NULL,
  `objetivo` varchar(150) DEFAULT NULL,
  `preferencias` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `experiencia` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `usuario`;
INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `correo`, `contraseña`, `edad`, `peso`, `altura`, `actividad`, `sexo`, `objetivo`, `preferencias`, `experiencia`) VALUES
	(6, 'Luis Angel', 'Romo Alvarado', 'luisangelromoalvarado@gma', 'scrypt:32768:8:1$3OvDpivyxyjCnVIN$4b502b3b12c8679e7a57c4d6f4edeee44e3ae237af40f8c8e780e3195120ab8bfee62d59debb31c520c1ec497b38cdfc32b1f067c171205f811e040bb3d73cf3', 17, 89, 1.83, 'ligera', 'Masculino', NULL, NULL, NULL),
	(7, 'Pedro', 'perez', 'hr@somecompany.com', 'scrypt:32768:8:1$e7pIWP49uirr26SV$4354b1b62d622e88b9790b82a3d6afb50d884f6f20f475eb7bda5b81b6de70077206e702f1ae48277c7f17ce55f3b5ebfe4b650f6150cee25d3a08dfd3cdbea1', 24, 79, 1.82, 'ligera', 'Masculino', 'mantener peso', '{\'alergia\': \'no\', \'alergias\': \'ninguno\', \'intolerancia\': \'gluten\', \'dietas\': \'vegetariana\', \'no_gusta\': \'nada\'}', 'intermedio'),
	(10, 'Angel', 'Guillermo', 'Angel@gmail.com', 'scrypt:32768:8:1$f5c95BUebb8H6dei$7a3e5a0ebf9b68e4294c901a3988e44fcb1c1571203375555b70ca5b8fc2c9fec88713a42c40a09d7b462363c11c7e7598c306180ab48ba06415b3d2b1f90a1d', 24, 95.5, 1.8, 'moderada', 'Masculino', NULL, NULL, NULL),
	(11, 'abril', 'perez', 'perez@gmail.com', 'scrypt:32768:8:1$RLS5YvrsO4f84TTJ$34979f3b1e0bfee4a863e92db54662c17448587c93f6300bbb94326476442795b1493f68ed2336ee45bd84c05b9837440cb889c459ddd6f33ab52a8a489c22d9', 47, 63, 1.65, 'moderada', 'Masculino', NULL, NULL, NULL),
	(12, 'lulu', 'londres', 'londres@gmail.com', 'scrypt:32768:8:1$yx4WGZTJ7kCiphHw$d76e097d771d96feddc271a62ee3a2b809b90e3e0c355c9b8b91a8ea35ea59abdc3a4add1374c40811463df412c822e285513abdf7cea6452797cbf893954d74', 26, 56, 1.54, 'ligera', 'Masculino', 'bajar de peso', '{\'alergia\': \'no\', \'alergias\': \'ninguno\', \'intolerancia\': \'no\', \'dietas\': \'ninguna\', \'no_gusta\': \'nada\'}', 'intermedio'),
	(13, 'prueba', 'Pruebas', 'prueba@gmail.com', 'scrypt:32768:8:1$LKgCbtN5JkFrSUqw$593db0c75dc2ca5657283622eb8dcd2d173b585e8ceccab4fc24913ec2572c2737d78aa64cfcd052639a8fc0f67d0fcda2624f757da03df18eda29550af727d3', 23, 1.54, 2.5, 'moderada', 'Masculino', 'bajar de peso', NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
