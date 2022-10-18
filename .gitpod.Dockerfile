FROM gitpod/workspace-mysql

RUN mysql -u root -p -e "create database researchprojectdb"
RUN mysql -u root -D researchprojectdb < ./researchprojectdb.sql