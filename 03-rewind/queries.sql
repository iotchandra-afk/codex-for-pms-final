-- Module 3: executed read-only queries, in extraction/audit order.
-- Source timestamps are local (timestamp without time zone). Weeks start Monday.
-- All available rows are exported; pagination stays below the 1,000-row tool cap.

-- audit
select 'pings' as source, count(*) as rows, min(sent_at) as first_at, max(sent_at) as last_at from pings union all select 'callouts', count(*), min(happened_at), max(happened_at) from callouts;

-- roster
select name, handler, area from responders order by name;

-- outcomes
select outcome, count(*) as pings from pings group by outcome order by outcome;

-- weekly
select date_trunc('week', sent_at)::date as week_start, count(*) as pings, count(*) filter (where outcome = 'taken') as taken, count(*) filter (where outcome = 'turned down') as turned_down, count(*) filter (where outcome = 'missed') as missed, round(100.0 * count(*) filter (where outcome = 'taken')/count(*), 2) as acceptance_pct from pings group by 1 order by 1;

-- ping_page_1
select callout_number, responder, sent_at, outcome from pings order by sent_at, callout_number, responder, outcome limit 800 offset 0;

-- ping_page_2
select callout_number, responder, sent_at, outcome from pings order by sent_at, callout_number, responder, outcome limit 800 offset 800;

-- ping_page_3
select callout_number, responder, sent_at, outcome from pings order by sent_at, callout_number, responder, outcome limit 800 offset 1600;

-- callout_page_1
select callout_number, happened_at, area, what_happened from callouts order by callout_number limit 800 offset 0;

-- callout_page_2
select callout_number, happened_at, area, what_happened from callouts order by callout_number limit 800 offset 800;

-- responder_weeks
with weeks as (select generate_series(date '2026-06-29', date '2026-08-31', interval '1 week')::date as week_start) select w.week_start, r.name as responder, r.handler, r.area, count(p.sent_at) as pings, count(*) filter (where p.outcome = 'taken') as taken, count(*) filter (where p.outcome = 'turned down') as turned_down, count(*) filter (where p.outcome = 'missed') as missed from weeks w cross join responders r left join pings p on p.responder = r.name and p.sent_at >= w.week_start and p.sent_at < w.week_start + interval '1 week' group by w.week_start, r.name, r.handler, r.area order by w.week_start, r.name;

-- quality
select
(select count(*) from pings where callout_number is null or responder is null or sent_at is null or outcome is null) as incomplete_pings,
(select count(*) from pings where outcome not in ('taken','turned down','missed')) as invalid_outcomes,
(select count(*) from (select callout_number,responder,sent_at,outcome from pings group by 1,2,3,4 having count(*)>1) d) as duplicate_ping_groups,
(select count(*) from (select callout_number from callouts group by 1 having count(*)>1) d) as duplicate_callout_numbers,
(select count(*) from pings p left join responders r on r.name=p.responder where r.name is null) as unknown_responders,
(select count(*) from pings p left join callouts c on c.callout_number=p.callout_number where c.callout_number is null) as orphan_pings,
(select count(*) from pings p join callouts c using(callout_number) where p.sent_at<c.happened_at) as pings_before_incident,
(select count(*) from (select callout_number from pings group by 1 having count(*) filter(where outcome='taken')>1) d) as callouts_with_multiple_taken;

-- area_weeks
select date_trunc('week', happened_at)::date as week_start, area, count(*) as callouts from callouts group by 1,2 order by 1,2;

-- periods
with classified as (select *,case when sent_at < timestamp '2026-08-10' then 'baseline_6_weeks' when sent_at < timestamp '2026-08-17' then 'release_week' else 'post_3_weeks' end as period from pings) select period,count(*) as pings,count(*) filter(where outcome='taken') as taken,count(*) filter(where outcome='turned down') as turned_down,count(*) filter(where outcome='missed') as missed,round(100.0*count(*) filter(where outcome='taken')/count(*),4) as acceptance_pct from classified group by period order by min(sent_at);

-- exact_date_periods
select case when sent_at < timestamp '2026-08-12' then 'before_12_aug' when sent_at < timestamp '2026-08-13' then 'on_12_aug' else 'after_12_aug' end as period,count(*) as pings,count(*) filter(where outcome='taken') as taken,count(*) filter(where outcome='turned down') as turned_down,count(*) filter(where outcome='missed') as missed from pings group by 1 order by min(sent_at);

-- cohort_sql
select case when responder in ('Farlight','Vesper','The Undertow','Meteor Mite') then 'severely_reduced_four' else 'other_twelve' end as cohort,case when sent_at<timestamp '2026-08-10' then 'baseline_6_weeks' when sent_at<timestamp '2026-08-17' then 'release_week' else 'post_3_weeks' end as period,count(*) as pings,count(*) filter(where outcome='taken') as taken,count(*) filter(where outcome='turned down') as turned_down,count(*) filter(where outcome='missed') as missed from pings group by 1,2 order by 1,min(sent_at);

-- join_timing_audit
select (select count(distinct sent_at::date) from pings) as ping_dates,(select count(distinct happened_at::date) from callouts) as callout_dates,(select count(*) from (select callout_number,sent_at from pings group by 1,2 having count(*)>1) s) as simultaneous_ping_groups,(select count(*) from pings p join callouts c using(callout_number) where date_trunc('week',p.sent_at)<>date_trunc('week',c.happened_at)) as pings_crossing_callout_week;

-- ticket_links
select ticket_number,filed_at,filed_by,about_responder,subject,body from support_tickets where about_responder in ('Farlight','The Undertow','Corporal Ashgrove','Halfmoon','Vesper','Meteor Mite','The Gale') and (subject like '%quiet%' or subject like '%Hardly%' or subject like '%has not gone off%' or subject like '%Nothing coming%' or subject like '%still on the list%' or subject like '%asked me to pass%' or subject like '%First one in%') order by filed_at;

-- callout_week_sql
with outcomes as (select callout_number,count(*) as ping_count,count(*) filter(where outcome='taken') as taken_count from pings group by 1) select date_trunc('week',c.happened_at)::date as week_start,count(*) as callouts,count(*) filter(where o.taken_count>0) as callouts_with_taken,count(*) filter(where coalesce(o.taken_count,0)=0) as callouts_without_taken,count(*) filter(where coalesce(o.ping_count,0)=0) as callouts_without_ping from callouts c left join outcomes o using(callout_number) group by 1 order by 1;

-- roster_audit
select (select count(*) from responders) as roster_rows,(select count(distinct name) from responders) as unique_responder_names,(select count(*) from responders where name is null or handler is null or area is null) as incomplete_roster_rows,(select count(*) from handlers) as handler_rows,(select count(distinct name) from handlers) as unique_handler_names,(select count(*) from responders r left join handlers h on h.name=r.handler where h.name is null) as unmatched_handlers;

-- cohort_area_sql
select area,case when happened_at<timestamp '2026-08-10' then 'baseline_6_weeks' when happened_at<timestamp '2026-08-17' then 'release_week' else 'post_3_weeks' end as period,count(*) as callouts from callouts where area in ('Uptown','Old Town','Harborside','Eastgate') group by 1,2 order by 1,min(happened_at);


