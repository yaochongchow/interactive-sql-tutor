Drop table IF EXISTS Friendship;
Drop table IF EXISTS Likes;
Create table Friendship (
user1_id int, 
user2_id int)
;
Create table Likes (
user_id int, 
page_id int)
;
insert into Friendship (user1_id, user2_id) values ('1', '2');
insert into Friendship (user1_id, user2_id) values ('1', '3');
insert into Friendship (user1_id, user2_id) values ('1', '4');
insert into Friendship (user1_id, user2_id) values ('2', '3');
insert into Friendship (user1_id, user2_id) values ('2', '4');
insert into Friendship (user1_id, user2_id) values ('2', '5');
insert into Friendship (user1_id, user2_id) values ('6', '1');
insert into Likes (user_id, page_id) values ('1', '88');
insert into Likes (user_id, page_id) values ('2', '23');
insert into Likes (user_id, page_id) values ('3', '24');
insert into Likes (user_id, page_id) values ('4', '56');
insert into Likes (user_id, page_id) values ('5', '11');
insert into Likes (user_id, page_id) values ('6', '33');
insert into Likes (user_id, page_id) values ('2', '77');
insert into Likes (user_id, page_id) values ('3', '77');
insert into Likes (user_id, page_id) values ('6', '88');