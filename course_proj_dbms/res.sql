INSERT INTO restaurant (r_id, name, location, cuisineType, password, email) 
VALUES (5, 'Royal China', '10/3, Elgin Rd, Sreepally, Bhowanipore, Kolkata, West Bengal 700020', 'Cantonese, Chinese', 'rc', 'forum@royalchinakolkata.com');
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (71, 'Royal China Chilli Chicken', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (72, 'Crispy Vegetable in Salt and Pepper', 555, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (73, 'Steamed Garlic Prawns', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (74, 'Sliced lamb with black pepper', 995, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (75, 'Vegetable hot and sour soup', 325, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (76, 'Chicken hot and sour soup', 345, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (77, 'Prawn wonton soup', 445, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (78, 'Fresh lobster served with noodles', 3295, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (79, 'Singapore chilli prawns', 975, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (80, 'bhetki', 2195, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (81, 'sliced fish', 645, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (82, 'sweet and sour chicken', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (83, 'roast chicken in burnt garlic', 895, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (84, 'szechuan chicken', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (85, 'cottage cheese with chilli oil', 575, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (86, 'kung pao potato with okra', 495, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (87, 'cantonese style chicken fried rice', 475, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (88, 'vegetable royal lotus leaf fried rice', 595, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (89, 'prawn wok tossed hakka noodles', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (89, 'prawn wok tossed hakka noodles', 775, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (90, 'vegetable ho fun noodles', 545, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (91, 'classic cheesecake', 395, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (92, 'royal caramel custard', 325, TRUE, 5);
INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id)
VALUES (93, 'variety of ice cream(3 scoops)', 195, TRUE, 5);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (21,'2024-03-31','00:00','2024-04-30','23:59',330);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (22,'2024-03-21','00:00','2024-04-29','23:59',3100);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (23,'2024-03-11','00:00','2024-05-30','23:59',950);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (24,'2024-03-06','00:00','2024-05-13','23:59',450);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (25,'2024-03-10','00:00','2024-05-05','23:59',375);
INSERT INTO offer (id,date_active_from,time_active_from,date_active_to,time_active_to,offer_price)
VALUES (26,'2024-03-08','00:00','2024-05-08','23:59',315);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (19,21,76);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (20,22,78);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (21,23,79);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (22,24,87);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (23,25,91);
INSERT INTO in_offer(id,offer_id,menu_item_id)
VALUES (24,26,92);