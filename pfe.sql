-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2025 at 03:51 PM
-- Server version: 10.6.15-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pfe`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_customuser`
--

CREATE TABLE `account_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_address` varchar(255) DEFAULT NULL,
  `company_website` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account_customuser`
--

INSERT INTO `account_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `verified`, `company_name`, `company_address`, `company_website`) VALUES
(1, '123pass123', '2025-04-06 14:45:08.000000', 1, 'ouahid11', '', '', '', 1, 1, '2025-03-14 23:12:55.000000', 'employee', 0, NULL, NULL, NULL),
(2, 'pbkdf2_sha256$870000$kJahdE93581tGsENIND6zz$Ca+11o0yhah0dieYJ5n6P2KQsmvUKaqMYhfkvojjaZM=', NULL, 0, 'john.doe@example.com', 'John', 'Doe', 'john.doe@example.com', 0, 1, '2025-03-14 23:13:37.000000', 'admin', 0, 'TechCorp', '123 Tech Street, City', 'https://www.techcorp.com'),
(3, '123pass123', NULL, 0, 'emppp', 'John', 'Doe', 'employee@gmail.com', 0, 1, '2025-04-05 13:12:57.000000', 'admin', 0, NULL, NULL, NULL),
(16, '123pass123', NULL, 0, 'emp', 'emp', 'emp', 'emp@gmail.com', 1, 1, '2025-04-07 19:38:50.000000', 'employer', 1, 'goes', 'ma', 'https://www.techcorp.com'),
(17, 'pbkdf2_sha256$870000$t7jBJf5oUTPB3JsGEyvpQh$k5dygQMreYTmJfNH/gOQpzx/EW8n8R1W2SW29loURcM=', NULL, 0, 'emp1@gmail.com', 'emp1', 'Doe', 'emp1@gmail.com', 0, 1, '2025-04-07 19:45:16.825011', 'employer', 0, NULL, NULL, NULL),
(18, 'pbkdf2_sha256$870000$nZbRuc85nJJPkwEsvEcWpW$sXW7W6wzMQkm8rAjynl4V7ijqnCbPrXyIA059qZPYcY=', '2025-04-07 21:23:46.711913', 1, 'admin', '', '', '', 1, 1, '2025-04-07 21:23:35.621778', 'employee', 0, NULL, NULL, NULL),
(19, 'pbkdf2_sha256$870000$7JUk9mk3BCUkuweGMCIPgq$2ftwgKdCl8ywt5PoZBNkwYAgXlTWpSo/ngbXGQkPUhU=', NULL, 1, 'newadmin@example.com', 'Admin', 'User', 'newadmin@example.com', 1, 1, '2025-04-08 20:48:44.179211', 'admin', 0, NULL, NULL, NULL),
(20, 'pbkdf2_sha256$870000$pAsIZmfZQCv42G3Xld7Dmc$AtzuraSlhZhZvF3/mMB0KaxSA2gKZl2zh3TWRthniKk=', NULL, 0, 'employer@test.com', 'Employer', 'Test', 'employer@test.com', 0, 1, '2025-04-08 20:59:23.059147', 'employer', 1, 'Test Corp', NULL, NULL),
(21, 'pbkdf2_sha256$870000$gbE1Ppm6QaYonqT7pMJHaY$5QuCs1KSXZNoaXq/1KVJvfoal0OW0C1o2V8qA904ke8=', NULL, 0, 'john_doe', 'John', 'Doe', 'john@example.com', 0, 1, '2025-04-08 21:26:51.652096', 'employer', 0, 'Tech Corp', NULL, NULL),
(22, 'pbkdf2_sha256$870000$14aL4ExSyc6lMnMJw10VbM$UMKFIVfo35ohjQCpQXOsNjl2BvPbjZhimpnBuWAUaWY=', NULL, 0, 'lshdkdsas@gmail.com', 'ouahid', 'ouahid', 'lshdkds13@gmail.com', 0, 1, '2025-04-09 15:19:26.843365', 'employee', 0, NULL, NULL, NULL),
(23, 'pbkdf2_sha256$870000$4s5OCPcKsLP2n3pj3bI2NZ$OJpWkhMh59HPJF46qtP9L0XSGNj60qQu0mt16E/EKTQ=', NULL, 0, 'lshdkdsaa@gmail.com', 'ouahidada', 'ouahidasa', 'lshdkds1asd2@gmail.com', 0, 1, '2025-04-09 15:25:48.000000', 'admin', 0, 'goes', 'ma', 'https://www.speedtest.net/'),
(24, '123pass123', '2025-04-10 11:37:09.000000', 0, 'emp11', '', '', 'emp11@gmail.com', 0, 1, '2025-04-10 11:37:02.000000', 'employee', 0, NULL, NULL, NULL),
(25, 'pbkdf2_sha256$870000$JIeVuEJHvaF8AjHmOZmWoz$zpAiFKmHQDp8U764pyuNGWsaYiS1oYd+zUBmleJcoa4=', NULL, 0, 'emp12', 'John', 'Doe', 'emp12@example.com', 0, 1, '2025-04-10 11:38:33.911567', 'employee', 0, NULL, NULL, NULL),
(26, 'pbkdf2_sha256$870000$bS7SV1Ajlhu7cgm7rwjnUf$43r3QpBDS/l9IZ5vinpBsqTH6Kecwjkg3qSVG4vVLoQ=', NULL, 0, 'ouahid samrani', 'ouahid', 'samrani', 'ouahidel1@gmail.com', 0, 1, '2025-04-10 12:02:55.209583', 'employee', 0, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `account_customuser_groups`
--

CREATE TABLE `account_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `account_customuser_user_permissions`
--

CREATE TABLE `account_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Token', 6, 'add_token'),
(22, 'Can change Token', 6, 'change_token'),
(23, 'Can delete Token', 6, 'delete_token'),
(24, 'Can view Token', 6, 'view_token'),
(25, 'Can add Token', 7, 'add_tokenproxy'),
(26, 'Can change Token', 7, 'change_tokenproxy'),
(27, 'Can delete Token', 7, 'delete_tokenproxy'),
(28, 'Can view Token', 7, 'view_tokenproxy'),
(29, 'Can add user', 8, 'add_customuser'),
(30, 'Can change user', 8, 'change_customuser'),
(31, 'Can delete user', 8, 'delete_customuser'),
(32, 'Can view user', 8, 'view_customuser'),
(33, 'Can add pdf document', 9, 'add_pdfdocument'),
(34, 'Can change pdf document', 9, 'change_pdfdocument'),
(35, 'Can delete pdf document', 9, 'delete_pdfdocument'),
(36, 'Can view pdf document', 9, 'view_pdfdocument'),
(37, 'Can add notification', 10, 'add_notification'),
(38, 'Can change notification', 10, 'change_notification'),
(39, 'Can delete notification', 10, 'delete_notification'),
(40, 'Can view notification', 10, 'view_notification'),
(41, 'Can add post', 11, 'add_post'),
(42, 'Can change post', 11, 'change_post'),
(43, 'Can delete post', 11, 'delete_post'),
(44, 'Can view post', 11, 'view_post'),
(45, 'Can add interview response', 12, 'add_interviewresponse'),
(46, 'Can change interview response', 12, 'change_interviewresponse'),
(47, 'Can delete interview response', 12, 'delete_interviewresponse'),
(48, 'Can view interview response', 12, 'view_interviewresponse'),
(49, 'Can add report', 13, 'add_report'),
(50, 'Can change report', 13, 'change_report'),
(51, 'Can delete report', 13, 'delete_report'),
(52, 'Can view report', 13, 'view_report'),
(53, 'Can add post application', 14, 'add_postapplication'),
(54, 'Can change post application', 14, 'change_postapplication'),
(55, 'Can delete post application', 14, 'delete_postapplication'),
(56, 'Can view post application', 14, 'view_postapplication'),
(57, 'Can add interview', 15, 'add_interview'),
(58, 'Can change interview', 15, 'change_interview'),
(59, 'Can delete interview', 15, 'delete_interview'),
(60, 'Can view interview', 15, 'view_interview');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-03-23 07:22:23.696155', '2', 'john.doe@example.com', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 8, 1),
(2, '2025-04-06 14:52:48.765935', '1', 'Entretien pour Python Developer -  (planned)', 1, '[{\"added\": {}}]', 15, 1),
(3, '2025-04-07 19:04:28.510490', '15', 'lshdkds121@gmail.com', 3, '', 8, 1),
(4, '2025-04-07 19:04:28.510490', '14', 'lshdkds11@gmail.com', 3, '', 8, 1),
(5, '2025-04-07 19:04:28.510490', '13', 'lshdkdd@gmail.com', 3, '', 8, 1),
(6, '2025-04-07 19:04:28.510490', '12', 'lshdkd@gmail.com', 3, '', 8, 1),
(7, '2025-04-07 19:04:28.510490', '11', 'lshdkdsa@gmail.com', 3, '', 8, 1),
(8, '2025-04-07 19:04:28.510490', '10', 'lshdkdsas@gmail.com', 3, '', 8, 1),
(9, '2025-04-07 19:04:28.510490', '9', 'lshdkdsouahid@gmail.com', 3, '', 8, 1),
(10, '2025-04-07 19:04:28.510490', '8', 'ouahid22@gmail.com', 3, '', 8, 1),
(11, '2025-04-07 19:04:28.510490', '7', 'employe@gmail.com', 3, '', 8, 1),
(12, '2025-04-07 19:04:28.510490', '6', 'lshdkds13@gmail.com', 3, '', 8, 1),
(13, '2025-04-07 19:04:28.510490', '5', 'lshdkds1@gmail.com', 3, '', 8, 1),
(14, '2025-04-07 19:04:28.510490', '4', 'lshdkds@gmail.com', 3, '', 8, 1),
(15, '2025-04-07 19:04:50.109782', '3', 'employee@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 8, 1),
(16, '2025-04-07 19:35:43.759069', '4', 'dd vv', 1, '[{\"added\": {}}]', 11, 1),
(17, '2025-04-07 19:39:58.144686', '16', 'emp', 1, '[{\"added\": {}}]', 8, 1),
(18, '2025-04-07 21:22:12.923886', '1', 'ouahid11', 2, '[{\"changed\": {\"fields\": [\"Password\"]}}]', 8, 1),
(19, '2025-04-09 15:29:08.280144', '23', 'lshdkdsaa@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 8, 18),
(20, '2025-04-10 11:34:29.873877', '3', 'employee@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Password\"]}}]', 8, 18),
(21, '2025-04-10 11:36:10.992426', '3', 'emppp', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 8, 18),
(22, '2025-04-10 11:37:34.985669', '24', 'emp11', 1, '[{\"added\": {}}]', 8, 18),
(23, '2025-04-10 11:53:56.697843', '9', 'Développeur asdfa ads', 2, '[{\"changed\": {\"fields\": [\"Description\"]}}]', 11, 18);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(8, 'account', 'customuser'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(6, 'authtoken', 'token'),
(7, 'authtoken', 'tokenproxy'),
(4, 'contenttypes', 'contenttype'),
(15, 'post', 'interview'),
(12, 'post', 'interviewresponse'),
(10, 'post', 'notification'),
(9, 'post', 'pdfdocument'),
(11, 'post', 'post'),
(14, 'post', 'postapplication'),
(13, 'post', 'report'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-03-14 23:11:57.782549'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-03-14 23:11:57.831477'),
(3, 'auth', '0001_initial', '2025-03-14 23:11:58.009002'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-03-14 23:11:58.046900'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-03-14 23:11:58.057873'),
(6, 'auth', '0004_alter_user_username_opts', '2025-03-14 23:11:58.067844'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-03-14 23:11:58.078815'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-03-14 23:11:58.080810'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-03-14 23:11:58.090785'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-03-14 23:11:58.100756'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-03-14 23:11:58.110683'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-03-14 23:11:58.138606'),
(13, 'auth', '0011_update_proxy_permissions', '2025-03-14 23:11:58.149577'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-03-14 23:11:58.159555'),
(15, 'account', '0001_initial', '2025-03-14 23:11:58.402898'),
(16, 'admin', '0001_initial', '2025-03-14 23:11:58.486077'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-03-14 23:11:58.497048'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-03-14 23:11:58.506024'),
(19, 'authtoken', '0001_initial', '2025-03-14 23:11:58.560878'),
(20, 'authtoken', '0002_auto_20160226_1747', '2025-03-14 23:11:58.589799'),
(21, 'authtoken', '0003_tokenproxy', '2025-03-14 23:11:58.593795'),
(22, 'authtoken', '0004_alter_tokenproxy_options', '2025-03-14 23:11:58.601768'),
(23, 'post', '0001_initial', '2025-03-14 23:11:58.928044'),
(24, 'sessions', '0001_initial', '2025-03-14 23:11:58.964945'),
(25, 'post', '0002_alter_interviewresponse_answer_and_more', '2025-03-15 23:13:27.147926'),
(26, 'post', '0003_post_salaire', '2025-04-05 00:07:05.578296'),
(27, 'post', '0004_delete_notification', '2025-04-05 11:25:13.766673'),
(28, 'post', '0005_remove_interviewresponse_approved', '2025-04-05 11:31:11.610295'),
(29, 'post', '0006_postapplication', '2025-04-05 13:03:59.934543'),
(30, 'post', '0007_postapplication_cv_postapplication_interview', '2025-04-05 17:35:20.013163'),
(31, 'post', '0008_report', '2025-04-05 22:51:03.647014'),
(32, 'post', '0009_interview', '2025-04-06 14:43:30.104405'),
(33, 'post', '0010_remove_post_accepted_postapplication_step_and_more', '2025-04-09 16:48:15.723971');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('bizahjblkv16s94jvhdzdzx05ynob0ah', '.eJxVjDsOwjAQBe_iGln-Y1PS5wzWrneFA8iW4qRC3B0ipYD2zcx7iQzbWvM2eMkziYvQ4vS7IZQHtx3QHdqty9Lbuswod0UedMipEz-vh_t3UGHUbw0-KPQUwYaz0WQsFKKEDgEoJGQIwKRcQrCcyFEMSlHRJSVlovdGvD8GdTiB:1ttEDI:EW8Z5CalaH2mUVktze21P64t62XjK-ToZyNjI4QzdgA', '2025-03-28 23:13:12.562055'),
('sivrkci6mop5035tub344w94fqgy60bl', '.eJxVjMsOwiAUBf-FtSFQSrl16d5vIPcBUjU0Ke3K-O_apAvdnpk5LxVxW0vcWlriJOqsLKjT70jIj1R3Inest1nzXNdlIr0r-qBNX2dJz8vh_h0UbOVbAwOnPPSdH6wDDOydtwlCyEaIRhy8AXAkvRBi9qNzWQiEE5vgutCp9wcQDzh3:1u1twY:70WfqOX9hhgyrdOqIZkwlkpWGf019V1cDHdA4B1mHXI', '2025-04-21 21:23:46.716583');

-- --------------------------------------------------------

--
-- Table structure for table `post_interview`
--

CREATE TABLE `post_interview` (
  `id` bigint(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `questions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`questions`)),
  `responses` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`responses`)),
  `score` double DEFAULT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_interview`
--

INSERT INTO `post_interview` (`id`, `status`, `start_date`, `end_date`, `questions`, `responses`, `score`, `post_id`, `user_id`) VALUES
(1, 'planned', '2025-04-06 14:45:43.000000', '2025-04-07 14:45:43.000000', NULL, NULL, NULL, 1, 1),
(2, 'planned', '2025-04-10 13:24:56.424649', '2025-04-11 13:24:56.424649', NULL, NULL, NULL, 9, 21);

-- --------------------------------------------------------

--
-- Table structure for table `post_interviewresponse`
--

CREATE TABLE `post_interviewresponse` (
  `id` bigint(20) NOT NULL,
  `question` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `score` double NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `post_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_interviewresponse`
--

INSERT INTO `post_interviewresponse` (`id`, `question`, `answer`, `timestamp`, `score`, `user_id`, `post_id`) VALUES
(1, 'What experience do you have with Python?', 'I have 3 years of experience with Python.', '2025-03-15 23:36:26.258647', 0, 2, 1),
(2, 'What experience do you have with Python?', 'I ha Python.', '2025-03-15 23:36:34.184421', 0, 2, 1),
(3, 'What experience do you have with Python?', 'I ha Python.', '2025-03-15 23:36:36.451659', 0, 2, 1),
(4, 'What experience do you have with Python?', 'I ha .', '2025-03-15 23:36:39.285447', 0, 2, 1),
(5, 'What experience do you have with Python?', 'I ha .', '2025-03-15 23:36:40.748175', 0, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `post_pdfdocument`
--

CREATE TABLE `post_pdfdocument` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `pdf_file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_pdfdocument`
--

INSERT INTO `post_pdfdocument` (`id`, `title`, `pdf_file`, `uploaded_at`) VALUES
(1, 'mon cv1', 'pdfs/Mohamed_Lachkar_lettre_de_motivation.pdf', '2025-03-15 23:31:41.146545'),
(2, 'Application for Développeur Test', 'pdfs/Irhil-Oussama-cv.pdf', '2025-04-09 15:22:13.755674'),
(3, 'mon cv', 'pdfs/cv1.pdf', '2025-04-10 11:43:11.554513');

-- --------------------------------------------------------

--
-- Table structure for table `post_post`
--

CREATE TABLE `post_post` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `final_date` date DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `salaire` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_post`
--

INSERT INTO `post_post` (`id`, `title`, `description`, `final_date`, `uploaded_at`, `user_id`, `salaire`) VALUES
(1, 'Python Developer', 'We are looking for a Python developer with Django experience.', '2023-12-31', '2025-03-14 23:16:41.467922', 2, NULL),
(2, 'Développeur Python', 'Recherche un développeur Python expérimenté.', '2025-04-01', '2025-03-15 23:21:17.886290', 2, NULL),
(3, 'Développeur Senior', 'Poste à pourvoir', '2025-04-01', '2025-04-05 13:10:10.733806', 2, 10000.00),
(5, 'Développeur back', 'Poste à pourvoir', '2025-04-01', '2025-04-07 21:27:12.212149', 17, 10000.00),
(6, 'Développeur Test', 'Poste de test', NULL, '2025-04-08 21:04:29.547585', 20, NULL),
(7, 'afda', 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf', '2025-05-09', '2025-04-09 15:27:03.670040', 23, 3223.00),
(8, ';dkfas;dljf', 'asd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfjasd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfjasd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfjasd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfjasd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfjasd;lfka ;fl sdf;lkjas df;laskjd f;asl f;alsdjkf ;asdlfkj a;slkdfj as;dlkfj', '2025-05-09', '2025-04-09 15:28:40.634155', 23, 2323.00),
(9, 'Développeur asdfa ads', 'First Last\r\nMachine Learning Engineer\r\nPhoenix, Ariizona • +1-234-456-789 • professionalemail@resumeworded.com • linkedin.com/in/username\r\nMachine learning engineer with 10 years of experience implementing statistical machine learning solutions and\r\ndemand forecasting models to improve forecast accuracy. Key achievement: optimized personalization algorithms\r\nfor 25+ applications with 372K users.\r\nRELEVANT WORK EXPERIENCE\r\n_______________________________________________________________________________________________________________\r\nResume Worded, New York, NY 2015 – Present\r\nMachine Learning Engineer\r\n● Tracked the health of 15+ robots using React/Redux with NodeJS backend and Python scripts, which\r\ncollected 100TB of data from its sensors.\r\n● Designed a deep learning model to detect and classify anomalies in the manufacturing process of 34+\r\nindustrial robots, reducing 83% of their monthly downtime.\r\n● Researched TensorFlow LSTM networks for speech recognition, OpenCV object tracking algorithms, and\r\n11+ new technologies; enhanced 74% of a dancing robot\'s performance.\r\n● Conceived and created a machine learning algorithm that detects deviant behavior in robots using SIFT,\r\nHOG, and 20+ other computer vision methods.\r\nGrowthsi, San Francisco, CA 2013 – 2015\r\nAutomation Engineer\r\n● Enhanced an automatic data processing machine performance by analyzing, testing, and debugging 2500+\r\nlines of code.\r\n● Developed work instructions and algorithms for 30+ newly installed hardware, converting Growthsi\r\nproduction floor from manual to 100% computer-controlled.\r\n● Established computerized process efficiency standards and implemented procedural controls; reduced\r\noverhead for 300+ clients and increased their annual sales profits by $150K YoY.\r\n● Created a computer program to monitor the performance of 45+ robotic arms and coordinate their\r\nfunctions based on the diagnostics from the computer.\r\nResume Worded Exciting Company, San Francisco, CA 2011 – 2013\r\nComputer Systems Analyst\r\n● Examined desktop usage patterns based on analysis of 10 TB of data from call center reports; created a\r\nsolution that boosted employee productivity by 78%.\r\n● Identified and resolved issues of network performance degradation, increasing system availability from 48%\r\nto 97% in the first month.\r\n● Designed algorithms to enhance data throughput between 50K mobile users and base stations while\r\nworking on the largest network upgrade for RWEC.\r\nEDUCATION\r\n_______________________________________________________________________________________________________________\r\nResume Worded University, New York, NY 2011\r\nBachelor of Science — Electrical Engineering and Computer Science\r\nSKILLS\r\n_______________________________________________________________________________________________________________\r\nTechnical Skills: Deep Learning (Advanced), Predictive Modeling (Experienced), Statistical Analysis, Algorithms\r\nLanguages: English (Native), German (Fluent), French (Conversational)', NULL, '2025-04-09 20:40:50.000000', 21, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `post_postapplication`
--

CREATE TABLE `post_postapplication` (
  `id` bigint(20) NOT NULL,
  `application_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `cv_id` bigint(20) DEFAULT NULL,
  `interview_id` bigint(20) DEFAULT NULL,
  `step` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_postapplication`
--

INSERT INTO `post_postapplication` (`id`, `application_date`, `status`, `post_id`, `user_id`, `cv_id`, `interview_id`, `step`) VALUES
(1, '2025-04-05 13:14:40.157944', 'en_attente', 3, 3, NULL, NULL, 'pending'),
(2, '2025-04-09 16:48:25.548718', 'refuse', 2, 21, 1, NULL, 'cv_compared'),
(3, '2025-04-09 20:58:09.289944', 'refuse', 5, 21, 1, NULL, 'cv_compared'),
(4, '2025-04-09 20:58:12.673163', 'refuse', 8, 21, 1, NULL, 'cv_compared'),
(5, '2025-04-09 20:58:16.195085', 'refuse', 1, 21, 1, NULL, 'cv_compared'),
(6, '2025-04-10 11:45:22.613813', 'refuse', 9, 21, 1, NULL, 'cv_compared'),
(7, '2025-04-10 11:54:05.510077', 'en_attente', 9, 21, 3, 2, 'interview_saved');

-- --------------------------------------------------------

--
-- Table structure for table `post_report`
--

CREATE TABLE `post_report` (
  `id` bigint(20) NOT NULL,
  `description` longtext NOT NULL,
  `reported_at` datetime(6) NOT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post_report`
--

INSERT INTO `post_report` (`id`, `description`, `reported_at`, `post_id`, `user_id`) VALUES
(1, 'fsad asdf', '2025-04-09 15:20:43.496568', 6, 22);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_customuser`
--
ALTER TABLE `account_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `account_customuser_groups`
--
ALTER TABLE `account_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_customuser_groups_customuser_id_group_id_7e51db7b_uniq` (`customuser_id`,`group_id`),
  ADD KEY `account_customuser_groups_group_id_2be9f6d7_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `account_customuser_user_permissions`
--
ALTER TABLE `account_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_customuser_user__customuser_id_permission_650e378f_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `account_customuser_u_permission_id_f4aec423_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_account_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `post_interview`
--
ALTER TABLE `post_interview`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_interview_post_id_2859ea37_fk_post_post_id` (`post_id`),
  ADD KEY `post_interview_user_id_7b5f0d71_fk_account_customuser_id` (`user_id`);

--
-- Indexes for table `post_interviewresponse`
--
ALTER TABLE `post_interviewresponse`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_interviewresponse_user_id_2e7b603d_fk_account_customuser_id` (`user_id`),
  ADD KEY `post_interviewresponse_post_id_241de321_fk_post_post_id` (`post_id`);

--
-- Indexes for table `post_pdfdocument`
--
ALTER TABLE `post_pdfdocument`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `post_post`
--
ALTER TABLE `post_post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_post_user_id_b9c97aef_fk_account_customuser_id` (`user_id`);

--
-- Indexes for table `post_postapplication`
--
ALTER TABLE `post_postapplication`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_postapplication_post_id_876d94b3_fk_post_post_id` (`post_id`),
  ADD KEY `post_postapplication_user_id_9618ab4b_fk_account_customuser_id` (`user_id`),
  ADD KEY `post_postapplication_cv_id_06e85e46_fk_post_pdfdocument_id` (`cv_id`),
  ADD KEY `post_postapplication_interview_id_a7d4305f_fk_post_interview_id` (`interview_id`);

--
-- Indexes for table `post_report`
--
ALTER TABLE `post_report`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_report_post_id_8c3c21d7_fk_post_post_id` (`post_id`),
  ADD KEY `post_report_user_id_2c7cb5b5_fk_account_customuser_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_customuser`
--
ALTER TABLE `account_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `account_customuser_groups`
--
ALTER TABLE `account_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_customuser_user_permissions`
--
ALTER TABLE `account_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `post_interview`
--
ALTER TABLE `post_interview`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `post_interviewresponse`
--
ALTER TABLE `post_interviewresponse`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `post_pdfdocument`
--
ALTER TABLE `post_pdfdocument`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `post_post`
--
ALTER TABLE `post_post`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `post_postapplication`
--
ALTER TABLE `post_postapplication`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `post_report`
--
ALTER TABLE `post_report`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_customuser_groups`
--
ALTER TABLE `account_customuser_groups`
  ADD CONSTRAINT `account_customuser_g_customuser_id_b6c60904_fk_account_c` FOREIGN KEY (`customuser_id`) REFERENCES `account_customuser` (`id`),
  ADD CONSTRAINT `account_customuser_groups_group_id_2be9f6d7_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `account_customuser_user_permissions`
--
ALTER TABLE `account_customuser_user_permissions`
  ADD CONSTRAINT `account_customuser_u_customuser_id_03bcc114_fk_account_c` FOREIGN KEY (`customuser_id`) REFERENCES `account_customuser` (`id`),
  ADD CONSTRAINT `account_customuser_u_permission_id_f4aec423_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `post_interview`
--
ALTER TABLE `post_interview`
  ADD CONSTRAINT `post_interview_post_id_2859ea37_fk_post_post_id` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`),
  ADD CONSTRAINT `post_interview_user_id_7b5f0d71_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `post_interviewresponse`
--
ALTER TABLE `post_interviewresponse`
  ADD CONSTRAINT `post_interviewresponse_post_id_241de321_fk_post_post_id` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`),
  ADD CONSTRAINT `post_interviewresponse_user_id_2e7b603d_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `post_post`
--
ALTER TABLE `post_post`
  ADD CONSTRAINT `post_post_user_id_b9c97aef_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `post_postapplication`
--
ALTER TABLE `post_postapplication`
  ADD CONSTRAINT `post_postapplication_cv_id_06e85e46_fk_post_pdfdocument_id` FOREIGN KEY (`cv_id`) REFERENCES `post_pdfdocument` (`id`),
  ADD CONSTRAINT `post_postapplication_interview_id_a7d4305f_fk_post_interview_id` FOREIGN KEY (`interview_id`) REFERENCES `post_interview` (`id`),
  ADD CONSTRAINT `post_postapplication_post_id_876d94b3_fk_post_post_id` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`),
  ADD CONSTRAINT `post_postapplication_user_id_9618ab4b_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);

--
-- Constraints for table `post_report`
--
ALTER TABLE `post_report`
  ADD CONSTRAINT `post_report_post_id_8c3c21d7_fk_post_post_id` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`),
  ADD CONSTRAINT `post_report_user_id_2c7cb5b5_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
