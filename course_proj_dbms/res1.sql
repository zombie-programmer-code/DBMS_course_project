INSERT INTO restaurant (r_id, name, location, cuisineType, password, email) 
VALUES (6, 'Riyasat', '375, Prince Anwar Shah Rd, South City Complex, Jadavpur, Kolkata, West Bengal 700068', 'North Indian', 'ri', 'southcitymall@riyasatkolkata.com');
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (94, 'Timatar Tulsi Shorva, Chilgoza', 295, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (95, 'Maraq (lamb stew)', 345, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (96, 'Aloo Soya Tikkia', 445, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (97, 'Kamal Kakadi Chaat', 395, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (98, 'Bhatti ka Chooza', 585, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (99, 'Shikanje ka Murgh', 585, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (100, 'Bhetki roller and chips', 675, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (101, 'Kebab Sampler', 895, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (102, 'Gobi Matar Makhana', 455, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (103, 'Khusk Mirch Panner', 565, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (104, 'Mardana Murgh', 595, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (105, 'Patiala Tawa Murg', 595, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (106, 'Safed Murg', 595, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (107, 'Chooza Dum Biriyani', 585, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (108, 'Naan', 130, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (109, 'Mirch Masala Kulcha', 155, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (110, 'Makhani Lachha Parantha', 135, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (111, 'Kesari Kulfi, Chia', 365, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (112, 'Baked Yoghurt, Fruits of the moment', 385, TRUE, 6);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (113, 'Sondesh Puff, Nolen Gurer', 385, TRUE, 6);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (27,'2024-03-29','00:00','2024-05-01','23:59',330);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (28,'2024-03-21','00:00','2024-06-29','23:59',560);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (29,'2024-03-11','00:00','2024-05-30','23:59',570);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (30,'2024-04-06','00:00','2024-05-23','23:59',145);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (31,'2024-03-10','00:00','2024-05-15','23:59',365);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (25,27,95);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (26,28,98);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (27,29,106);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (28,30,109);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (29,31,112);
