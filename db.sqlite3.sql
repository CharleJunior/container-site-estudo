BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "main_mural" (
	"id"	integer NOT NULL,
	"texto"	text NOT NULL,
	"autor_id"	integer,
	"data"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("autor_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "paineladmin_mural" (
	"id"	integer NOT NULL,
	"texto"	text NOT NULL,
	"data"	datetime NOT NULL,
	"autor_id"	integer,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("autor_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,3,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,3,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,3,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,3,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,2,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,2,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,2,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,2,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_mural','Can add mural');
INSERT INTO "auth_permission" VALUES (26,7,'change_mural','Can change mural');
INSERT INTO "auth_permission" VALUES (27,7,'delete_mural','Can delete mural');
INSERT INTO "auth_permission" VALUES (28,7,'view_mural','Can view mural');
INSERT INTO "auth_permission" VALUES (29,8,'add_accessattempt','Can add access attempt');
INSERT INTO "auth_permission" VALUES (30,8,'change_accessattempt','Can change access attempt');
INSERT INTO "auth_permission" VALUES (31,8,'delete_accessattempt','Can delete access attempt');
INSERT INTO "auth_permission" VALUES (32,8,'view_accessattempt','Can view access attempt');
INSERT INTO "auth_permission" VALUES (33,11,'add_accesslog','Can add access log');
INSERT INTO "auth_permission" VALUES (34,11,'change_accesslog','Can change access log');
INSERT INTO "auth_permission" VALUES (35,11,'delete_accesslog','Can delete access log');
INSERT INTO "auth_permission" VALUES (36,11,'view_accesslog','Can view access log');
INSERT INTO "auth_permission" VALUES (37,10,'add_accessfailurelog','Can add access failure');
INSERT INTO "auth_permission" VALUES (38,10,'change_accessfailurelog','Can change access failure');
INSERT INTO "auth_permission" VALUES (39,10,'delete_accessfailurelog','Can delete access failure');
INSERT INTO "auth_permission" VALUES (40,10,'view_accessfailurelog','Can view access failure');
INSERT INTO "auth_permission" VALUES (41,9,'add_accessattemptexpiration','Can add access attempt expiration');
INSERT INTO "auth_permission" VALUES (42,9,'change_accessattemptexpiration','Can change access attempt expiration');
INSERT INTO "auth_permission" VALUES (43,9,'delete_accessattemptexpiration','Can delete access attempt expiration');
INSERT INTO "auth_permission" VALUES (44,9,'view_accessattemptexpiration','Can view access attempt expiration');
INSERT INTO "auth_permission" VALUES (45,12,'add_mural','Can add mural');
INSERT INTO "auth_permission" VALUES (46,12,'change_mural','Can change mural');
INSERT INTO "auth_permission" VALUES (47,12,'delete_mural','Can delete mural');
INSERT INTO "auth_permission" VALUES (48,12,'view_mural','Can view mural');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$1200000$TWeuS72SAaBsLL1iis6Me1$wuSPkjKWwB6e+jLWvTQcrGE6QVTowOSBU/b7wyejwl0=','2026-04-18 22:49:19.954225',0,'Charle da Paixão Sousa Junior','','charledapaixaosousajunior@gmail.com',1,1,'2026-03-07 05:35:52.878655','');
INSERT INTO "auth_user" VALUES (2,'pbkdf2_sha256$1200000$lz3I2HzsjxxGnLgZ3tXqt7$bUoYfayHYZIWfvSIK7EJq9YD8JsbS91zCNglREeNEN8=','2026-03-07 05:54:46.229832',0,'CharleJunio','','charljdev@proton.me',0,0,'2026-03-07 05:49:48.042853','');
INSERT INTO "auth_user" VALUES (3,'argon2$argon2id$v=19$m=102400,t=2,p=8$am1qbmVOSzVoeVpXenpZNkpHYWFhUQ$5P0V0LdMvPd6WWX8i8WXIQIgOfYVCMKYlYCXF4RhSEQ','2026-04-18 22:19:02.226854',1,'admin','','',1,1,'2026-03-07 06:04:55.459694','');
INSERT INTO "auth_user" VALUES (4,'argon2$argon2id$v=19$m=102400,t=2,p=8$WFdWZFZ4a0x4ZERkcGhaTDBXbGQ1aQ$GA+hJ2om7Jf1/sOui9ghoc9ToroBq2mVpdL1mPqasTc','2026-04-09 22:27:11.944026',0,'user_normal','','charjdev@proton.me',0,0,'2026-04-09 22:07:29.737103','');
INSERT INTO "auth_user" VALUES (5,'!oZ0lFjZcdcdeMz2InFIppCoRyJ4tonjHr2ttMWWf','2026-04-19 00:30:30.849014',0,'Conta teste','','megawapps@gmail.com',0,1,'2026-04-11 18:32:24.083822','');
INSERT INTO "django_admin_log" VALUES (1,'1','Mural object (1)',1,'[{"added": {}}]',7,3,'2026-03-07 06:05:36.433941');
INSERT INTO "django_admin_log" VALUES (2,'1','Mural object (1)',2,'[{"changed": {"fields": ["Texto"]}}]',7,3,'2026-03-07 06:20:14.308987');
INSERT INTO "django_admin_log" VALUES (3,'1','Mural object (1)',2,'[{"changed": {"fields": ["Texto"]}}]',7,3,'2026-03-21 18:42:39.151146');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','group');
INSERT INTO "django_content_type" VALUES (3,'auth','permission');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_content_type" VALUES (7,'main','mural');
INSERT INTO "django_content_type" VALUES (8,'axes','accessattempt');
INSERT INTO "django_content_type" VALUES (9,'axes','accessattemptexpiration');
INSERT INTO "django_content_type" VALUES (10,'axes','accessfailurelog');
INSERT INTO "django_content_type" VALUES (11,'axes','accesslog');
INSERT INTO "django_content_type" VALUES (12,'paineladmin','mural');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2026-03-05 18:02:16.896964');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2026-03-05 18:02:16.929218');
INSERT INTO "django_migrations" VALUES (3,'admin','0001_initial','2026-03-05 18:02:16.950330');
INSERT INTO "django_migrations" VALUES (4,'admin','0002_logentry_remove_auto_add','2026-03-05 18:02:16.972061');
INSERT INTO "django_migrations" VALUES (5,'admin','0003_logentry_add_action_flag_choices','2026-03-05 18:02:16.984351');
INSERT INTO "django_migrations" VALUES (6,'contenttypes','0002_remove_content_type_name','2026-03-05 18:02:17.017554');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2026-03-05 18:02:17.037442');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2026-03-05 18:02:17.055146');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2026-03-05 18:02:17.068931');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2026-03-05 18:02:17.089704');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2026-03-05 18:02:17.094046');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2026-03-05 18:02:17.107380');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2026-03-05 18:02:17.127063');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2026-03-05 18:02:17.152073');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2026-03-05 18:02:17.170875');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2026-03-05 18:02:17.183226');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2026-03-05 18:02:17.202225');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2026-03-05 18:02:17.212964');
INSERT INTO "django_migrations" VALUES (19,'main','0001_initial','2026-03-07 06:02:51.543629');
INSERT INTO "django_migrations" VALUES (20,'axes','0001_initial','2026-03-21 18:23:12.281306');
INSERT INTO "django_migrations" VALUES (21,'axes','0002_auto_20151217_2044','2026-03-21 18:23:12.343904');
INSERT INTO "django_migrations" VALUES (22,'axes','0003_auto_20160322_0929','2026-03-21 18:23:12.364746');
INSERT INTO "django_migrations" VALUES (23,'axes','0004_auto_20181024_1538','2026-03-21 18:23:12.387942');
INSERT INTO "django_migrations" VALUES (24,'axes','0005_remove_accessattempt_trusted','2026-03-21 18:23:12.404031');
INSERT INTO "django_migrations" VALUES (25,'axes','0006_remove_accesslog_trusted','2026-03-21 18:23:12.422591');
INSERT INTO "django_migrations" VALUES (26,'axes','0007_alter_accessattempt_unique_together','2026-03-21 18:23:12.449096');
INSERT INTO "django_migrations" VALUES (27,'axes','0008_accessfailurelog','2026-03-21 18:23:12.463345');
INSERT INTO "django_migrations" VALUES (28,'axes','0009_add_session_hash','2026-03-21 18:23:12.478559');
INSERT INTO "django_migrations" VALUES (29,'axes','0010_accessattemptexpiration','2026-03-21 18:23:12.488357');
INSERT INTO "django_migrations" VALUES (30,'paineladmin','0001_initial','2026-04-19 01:20:20.992535');
INSERT INTO "django_migrations" VALUES (31,'main','0002_remove_mural_data_criacao_mural_autor_mural_data','2026-04-19 02:00:10.580248');
INSERT INTO "django_session" VALUES ('r5lsp91pfgoinw1ic3ki5fm0xdtxswt1','.eJxVjEEOwiAQAP-yZ0PYAgV69O4byLKAVA1NSnsy_t006UGvM5N5Q6B9q2HveQ1zggkUXH5ZJH7mdoj0oHZfBC9tW-cojkSctovbkvLrerZ_g0q9wgSobHEsyY_oktFofbRKS4O2JObBcEzeM6HHsUjpFGuNrDxmZXEgaeDzBcS9Nts:1vyky0:Z0lp38pc2FaoxqiXYd6pvbAEjgYPwiW3TfOI7UUDCx8','2026-03-21 06:16:48.029825');
INSERT INTO "django_session" VALUES ('2r6xtneyoo9pna4w7ccd4xf4kpl46h3k','.eJxVjMsOwiAQAP9lz4aA7bLQo_d-A1leUjWQlPZk_HfTpAe9zkzmDY73rbi9p9UtESYY4PLLPIdnqoeID673JkKr27p4cSTitF3MLabX7Wz_BoV7gQmSSihtUKQV2cCjZiON1dJ4GvxoEjJaHTNFlZEwBiuzGjizQdLmGiR8vs0DN18:1w41GD:8sfe4Kstk8ZQLaIoysl8n1akFa12qyFIw96XZe4Ga_A','2026-04-04 18:41:21.155993');
INSERT INTO "django_session" VALUES ('9vi74qem84bd9g9yfu1mw0cwgyzln56f','.eJxVjMsKwjAQAP9lzxKaR5vQo3e_IWx2N6YqCTTtSfx3KfSg15lh3hBx30rcu6xxYZjBweWXJaSn1EPwA-u9KWp1W5ekjkSdtqtbY3ldz_ZvULAXmCFlYkcYTODgyYm2RrPRgxXkUTxl1FoSivMebTbTMI3Z6kDJCVmbA3y-Cx84sw:1wAxqB:yfJY3z1k4eQuYfCU-3goq5Ro1YrqhGdn7ZYwQH0gHZM','2026-04-23 22:27:11.951642');
INSERT INTO "main_mural" VALUES (1,'Protegido para os adms',NULL,'2026-04-19 02:00:10.576247');
INSERT INTO "main_mural" VALUES (2,'Charle junior passou por aquii',1,'2026-04-19 02:00:32.892790');
INSERT INTO "main_mural" VALUES (3,'Aviso importante 
',5,'2026-04-19 02:01:19.213624');
INSERT INTO "main_mural" VALUES (4,'Aviso do charle junior
',1,'2026-04-19 02:15:31.675613');
INSERT INTO "paineladmin_mural" VALUES (1,'','2026-04-19 01:29:59.469725',1);
INSERT INTO "paineladmin_mural" VALUES (2,'Olá','2026-04-19 01:36:19.799868',1);
INSERT INTO "paineladmin_mural" VALUES (3,'Olá','2026-04-19 01:48:44.795673',1);
INSERT INTO "paineladmin_mural" VALUES (4,'Mensagem legal','2026-04-19 01:54:55.613657',1);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "main_mural_autor_id_f95cfe23" ON "main_mural" (
	"autor_id"
);
CREATE INDEX IF NOT EXISTS "paineladmin_mural_autor_id_c13eed0f" ON "paineladmin_mural" (
	"autor_id"
);
COMMIT;
