** To create a new ppss_auth db revision:
cd ppss_auth/alembic
alembic -c alembic.ini revision --autogenerate -m "your comment here"
** then execute it with
alembic -c alembic.ini upgrade head

** babel/i18n
requires
apt install gettext
pip install babel

#extract strings from py, jinja2, mako
pybabel extract -F babel.ini -o ${project}/locale/${project}.pot ${project} 
#pybabel extract -F babel.ini -k _t:2 -o ${project}/locale/${project}.pot ${project} 
##for ppss_auth: 
pybabel extract -F babel.ini -o ppss_auth/locale/ppss_auth.pot ppss_auth



#first time creation
mkdir -p ${project}/${lang}/LC_MESSAGES
msginit -l ${lang} -o ${project}/locale/${lang}/LC_MESSAGES/${project}.po --input ${project}/locale/${project}.pot



#update
msgmerge --update ${project}/locale/${lang}/LC_MESSAGES/${project}.po ${project}/locale/${project}.pot
##for ppss_auth: 
msgmerge --update ppss_auth/locale/it/LC_MESSAGES/ppss_auth.po ppss_auth/locale/ppss_auth.pot
msgmerge --update ppss_auth/locale/en/LC_MESSAGES/ppss_auth.po ppss_auth/locale/ppss_auth.pot



#compile .po into .mo
msgfmt -o ${project}/locale/${lang}/LC_MESSAGES/${project}.mo ${project}/locale/${lang}/LC_MESSAGES/${project}.po
##for ppss_auth: 
msgfmt -o ppss_auth/locale/it/LC_MESSAGES/ppss_auth.mo ppss_auth/locale/it/LC_MESSAGES/ppss_auth.po
msgfmt -o ppss_auth/locale/en/LC_MESSAGES/ppss_auth.mo ppss_auth/locale/en/LC_MESSAGES/ppss_auth.po


##useful view for manual queries:
create view ppssauth_user_view as
select distinct 
    u.id as user_id,
    u.username as user_name ,
    u.enabled as enabled,
    p.name as permission 
from ppss_permission as p
    inner join ppssgroup_lk_ppsspermission as glkp on glkp.permission_id = p.id
    inner join ppss_group as g on glkp.group_id = g.id
    inner join ppssuser_lk_ppssgroup as ulkg on ulkg.group_id = glkp.group_id
    inner join ppss_user as u on u.id = ulkg.user_id
where g.enabled = 1;


create view ppssauth_user_groups as
select
    u.id as user_id,
    u.username as user_name ,
    u.enabled as user_enabled,
    g.id as group_id,
    g.name as group_name,
    g.enabled as group_enabled
from ppss_user as u
    inner join ppssuser_lk_ppssgroup as u_lk_g on u.id = u_lk_g.user_id
    inner join ppss_group as g on u_lk_g.group_id = g.id;

CREATE VIEW `ppssauth_groups_permission` AS 
select 
    `g`.`id` AS `group_id`,
    `g`.`name` AS `group_name`,
    `g`.`enabled` AS `group_enabled`,
    `p`.`id` AS `permission_id`,
    `p`.`name` AS `permission_name` 
from ((`ppss_group` `g` 
    join `ppssgroup_lk_ppsspermission` `g_lk_p` on((`g`.`id` = `g_lk_p`.`group_id`))) 
    join `ppss_permission` `p` on((`g_lk_p`.`permission_id` = `p`.`id`)));
