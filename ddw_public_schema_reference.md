# DDW Timescale DB - public Schema Reference

## Table: `2`
| Column Name | Data Type |
| ----------- | --------- |
| pt | USER-DEFINED |
| gps_time | text |
| gdir | integer |
| speed | integer |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `bi_eq`
| Column Name | Data Type |
| ----------- | --------- |
| bi_eq_tml_id | character varying |
| bi_eq_tml_gp | character varying |
| bi_eq_eq_no | character varying |
| bi_eq_eq_type | character varying |
| bi_eq_remove_flag | character varying |

## Table: `bi_eq_breaktime`
| Column Name | Data Type |
| ----------- | --------- |
| bi_eb_tml_id | character varying |
| bi_eb_eq_brk_seq | character varying |
| bi_eb_tml_gp | character varying |
| bi_eb_eq_no | character varying |
| bi_eb_eq_type | character varying |
| bi_eb_brk_start_time | timestamp without time zone |
| bi_eb_brk_end_time | timestamp without time zone |
| bi_eb_brk_code | character varying |

## Table: `bi_eq_geo_event`
| Column Name | Data Type |
| ----------- | --------- |
| bi_ge_event_seq | integer |
| bi_ge_tml_id | character varying |
| bi_ge_tml_gp | character varying |
| bi_ge_eq_no | character varying |
| bi_ge_eq_type | character varying |
| bi_ge_geo_type | character varying |
| bi_ge_geo_id | integer |
| bi_ge_geo_name | character varying |
| bi_ge_in_time | timestamp without time zone |
| bi_ge_out_time | timestamp without time zone |
| bi_ge_no_out_event | boolean |

## Table: `bi_eq_ignition`
| Column Name | Data Type |
| ----------- | --------- |
| bi_eg_eq_ign_seq | integer |
| bi_eg_tml_id | character varying |
| bi_eg_tml_gp | character varying |
| bi_eg_eq_no | character varying |
| bi_eg_eq_type | character varying |
| bi_eg_ign_on_time | timestamp without time zone |
| bi_eg_ign_off_time | timestamp without time zone |
| bi_eg_ign_off_source | character varying |

## Table: `bi_eq_job_event`
| Column Name | Data Type |
| ----------- | --------- |
| bi_je_eq_job_seq | integer |
| bi_je_tml_id | character varying |
| bi_je_tml_gp | character varying |
| bi_je_event_time | timestamp without time zone |
| bi_je_event_type | character varying |
| bi_je_eq_no | character varying |
| bi_je_eq_type | character varying |
| bi_je_eq_tran_id | character varying |
| bi_je_event_gen_type | character varying |
| bi_je_event_contents | jsonb |

## Table: `bi_eq_login`
| Column Name | Data Type |
| ----------- | --------- |
| bi_el_tml_id | character varying |
| bi_el_eq_log_seq | character varying |
| bi_el_tml_gp | character varying |
| bi_el_eq_no | character varying |
| bi_el_eq_type | character varying |
| bi_el_log_in_time | timestamp without time zone |
| bi_el_log_out_time | timestamp without time zone |
| bi_el_user_id | character varying |
| bi_el_shift_no | character varying |
| bi_el_first_name | character varying |
| bi_el_tel | character varying |

## Table: `bi_eq_tran`
| Column Name | Data Type |
| ----------- | --------- |
| bi_et_tml_id | character varying |
| bi_et_tml_gp | character varying |
| bi_et_eq_tran_id | character varying |
| bi_et_eq_no | character varying |
| bi_et_eq_type | character varying |
| bi_et_first_job_fetching_time | timestamp without time zone |
| bi_et_last_job_cmpl_time | timestamp without time zone |
| bi_et_trv_dist | integer |
| bi_et_fuel | integer |
| bi_et_event_step | jsonb |

## Table: `bi_eq_travel`
| Column Name | Data Type |
| ----------- | --------- |
| bi_ev_trv_seq | integer |
| bi_ev_tml_id | character varying |
| bi_ev_tml_gp | character varying |
| bi_ev_eq_no | character varying |
| bi_ev_eq_type | character varying |
| bi_ev_trv_stime | timestamp without time zone |
| bi_ev_trv_etime | timestamp without time zone |
| bi_ev_dist | numeric |
| bi_ev_fuel | integer |

## Table: `bi_eq_travel_job`
| Column Name | Data Type |
| ----------- | --------- |
| bi_tj_trv_seq | bigint |
| bi_tj_eq_tran_id | character varying |
| bi_tj_dist | numeric |
| bi_tj_fuel | integer |

## Table: `bi_job_hist`
| Column Name | Data Type |
| ----------- | --------- |
| bi_jh_job_hist_seq | integer |
| bi_jh_tml_id | character varying |
| bi_jh_tml_gp | character varying |
| bi_jh_job_id | character varying |
| bi_jh_job_type | character varying |
| bi_jh_eq_no | character varying |
| bi_jh_eq_type | character varying |
| bi_jh_mission_id | character varying |
| bi_jh_cntr_no | character varying |
| bi_jh_cntr_attr | jsonb |
| bi_jh_eq_tran_id | character varying |
| bi_jh_org_job_fetching_time | timestamp without time zone |
| bi_jh_job_fetching_time | timestamp without time zone |
| bi_jh_job_cmpl_time | timestamp without time zone |
| bi_jh_from_job_cmpl_time | timestamp without time zone |
| bi_jh_from_loc | character varying |
| bi_jh_from_eq_no | character varying |
| bi_jh_to_loc | character varying |
| bi_jh_to_eq_no | character varying |
| bi_jh_job_cycle_step | jsonb |
| bi_jh_trv_with_eta | jsonb |
| bi_jh_fuel | integer |
| bi_jh_user_id | character varying |
| bi_jh_shift_no | character varying |

## Table: `bi_job_mon`
| Column Name | Data Type |
| ----------- | --------- |
| bi_jm_tml_id | character varying |
| bi_jm_tml_gp | character varying |
| bi_jm_job_id | character varying |
| bi_jm_job_type | character varying |
| bi_jm_eq_no | character varying |
| bi_jm_eq_type | character varying |
| bi_jm_mission_id | character varying |
| bi_jm_cntr_no | character varying |
| bi_jm_cntr_attr | jsonb |
| bi_jm_eq_tran_id | character varying |
| bi_jm_job_fetching_time | timestamp without time zone |
| bi_jm_job_cmpl_time | timestamp without time zone |
| bi_jm_from_job_cmpl_time | timestamp without time zone |
| bi_jm_from_loc | character varying |
| bi_jm_from_eq_no | character varying |
| bi_jm_to_loc | character varying |
| bi_jm_to_eq_no | character varying |
| bi_jm_last_job_step | character varying |
| bi_jm_last_job_step_time | timestamp without time zone |

## Table: `bi_oee_tml_value`
| Column Name | Data Type |
| ----------- | --------- |
| bi_ov_value_seq | integer |
| bi_ov_tml_id | character varying |
| bi_ov_tml_gp | character varying |
| bi_ov_eq_type | character varying |
| bi_ov_value_type | character varying |
| bi_ov_value_desc | character varying |
| bi_ov_value | character varying |

## Table: `device_event`
| Column Name | Data Type |
| ----------- | --------- |
| deid | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| type | character varying |
| evt_cd | character varying |
| evt_dtl | character varying |
| contents | jsonb |
| create_time | timestamp without time zone |

## Table: `geography_columns`
| Column Name | Data Type |
| ----------- | --------- |
| f_table_catalog | name |
| f_table_schema | name |
| f_table_name | name |
| f_geography_column | name |
| coord_dimension | integer |
| srid | integer |
| type | text |

## Table: `geometry_columns`
| Column Name | Data Type |
| ----------- | --------- |
| f_table_catalog | character varying |
| f_table_schema | name |
| f_table_name | name |
| f_geometry_column | name |
| coord_dimension | integer |
| srid | integer |
| type | character varying |

## Table: `msg_bi_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_eq_agg_5min`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| eqty | character varying |
| cons | bigint |
| dist | bigint |
| type | character varying |
| contents | jsonb |
| create_time | timestamp without time zone |

## Table: `msg_eq_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_event_history`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_gis_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_int_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_iris_error`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_job_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_periodic_armgc`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_periodic_history`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_periodic_qc`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_periodic_rtls`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_periodic_rtls_all`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tiot_alarm`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tiot_delayed`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tiot_error`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tiot_event`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tos_in`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_tos_out`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `msg_vt_event`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| teid | character varying |
| uidt | bigint |
| utct | timestamp without time zone |
| vers | character varying |
| deid | character varying |
| tgrp | character varying |
| eqnm | character varying |
| type | character varying |
| contents | jsonb |
| eqty | character varying |
| create_time | timestamp without time zone |

## Table: `pg`
| Column Name | Data Type |
| ----------- | --------- |
| ogc_fid | integer |
| wkb_geometry | USER-DEFINED |
| gfc_tml_id | character varying |
| gfc_gfc_id | numeric |
| gfc_gfc_nm | character varying |
| gfc_gfc_tp | character varying |
| gfc_gfc_st | character varying |
| gfc_cre_ui | character varying |
| gfc_cre_da | timestamp with time zone |
| gfc_upd_ui | character varying |
| gfc_upd_da | timestamp with time zone |
| gfc_gfc_ds | character varying |
| gfc_gfc_ar | double precision |

## Table: `qrtz_blob_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| blob_data | bytea |

## Table: `qrtz_calendars`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| calendar_name | character varying |
| calendar | bytea |

## Table: `qrtz_cron_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| cron_expression | character varying |
| time_zone_id | character varying |

## Table: `qrtz_fired_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| entry_id | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| instance_name | character varying |
| fired_time | bigint |
| sched_time | bigint |
| priority | integer |
| state | character varying |
| job_name | character varying |
| job_group | character varying |
| is_nonconcurrent | boolean |
| requests_recovery | boolean |

## Table: `qrtz_job_details`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| job_name | character varying |
| job_group | character varying |
| description | character varying |
| job_class_name | character varying |
| is_durable | boolean |
| is_nonconcurrent | boolean |
| is_update_data | boolean |
| requests_recovery | boolean |
| job_data | bytea |

## Table: `qrtz_locks`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| lock_name | character varying |

## Table: `qrtz_paused_trigger_grps`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_group | character varying |

## Table: `qrtz_scheduler_state`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| instance_name | character varying |
| last_checkin_time | bigint |
| checkin_interval | bigint |

## Table: `qrtz_simple_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| repeat_count | bigint |
| repeat_interval | bigint |
| times_triggered | bigint |

## Table: `qrtz_simprop_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| str_prop_1 | character varying |
| str_prop_2 | character varying |
| str_prop_3 | character varying |
| int_prop_1 | integer |
| int_prop_2 | integer |
| long_prop_1 | bigint |
| long_prop_2 | bigint |
| dec_prop_1 | numeric |
| dec_prop_2 | numeric |
| bool_prop_1 | boolean |
| bool_prop_2 | boolean |

## Table: `qrtz_triggers`
| Column Name | Data Type |
| ----------- | --------- |
| sched_name | character varying |
| trigger_name | character varying |
| trigger_group | character varying |
| job_name | character varying |
| job_group | character varying |
| description | character varying |
| next_fire_time | bigint |
| prev_fire_time | bigint |
| priority | integer |
| trigger_state | character varying |
| trigger_type | character varying |
| start_time | bigint |
| end_time | bigint |
| calendar_name | character varying |
| misfire_instr | smallint |
| job_data | bytea |

## Table: `spatial_ref_sys`
| Column Name | Data Type |
| ----------- | --------- |
| srid | integer |
| auth_name | character varying |
| auth_srid | integer |
| srtext | character varying |
| proj4text | character varying |

## Table: `temp_geo_grid_map`
| Column Name | Data Type |
| ----------- | --------- |
| id | integer |
| geom | USER-DEFINED |

## Table: `tiot_border_status`
| Column Name | Data Type |
| ----------- | --------- |
| job_date | character varying |
| job_type | character varying |
| job_detail | jsonb |
| create_time | timestamp without time zone |
| update_time | timestamp without time zone |

## Table: `tiot_itv_status`
| Column Name | Data Type |
| ----------- | --------- |
| job_date | character varying |
| job_type | character varying |
| job_itv_no | character varying |
| job_event | character varying |
| job_detail | jsonb |
| create_time | timestamp without time zone |
| update_time | timestamp without time zone |

## Table: `tiot_job_time_interval`
| Column Name | Data Type |
| ----------- | --------- |
| job_interval_date | character varying |
| job_interval_hour | character varying |
| job_group_type | character varying |
| job_group_no | character varying |
| job_action_cnt | integer |
| job_type_detail | jsonb |
| create_time | timestamp without time zone |
| update_time | timestamp without time zone |

## Table: `tiot_job_time_interval_stat`
| Column Name | Data Type |
| ----------- | --------- |
| job_interval_year | character varying |
| job_interval_month | character varying |
| job_interval_day | character varying |
| job_group_type | character varying |
| job_group_no | character varying |
| job_action_cnt | integer |
| job_type_detail | jsonb |
| create_time | timestamp without time zone |
| update_time | timestamp without time zone |

## Table: `tiot_jobcycle`
| Column Name | Data Type |
| ----------- | --------- |
| utct | timestamp without time zone |
| cont_no | character varying |
| start_time | character varying |
| end_time | character varying |
| job_total | jsonb |
| job_detail | jsonb |
| create_time | timestamp without time zone |
| remake_yn | character varying |

## Table: `tiot_scheduler`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| job_name | character varying |
| start_utct | timestamp without time zone |
| end_utct | timestamp without time zone |
| job_limit_cnt | integer |
| job_tot_cnt | integer |
| job_suc_cnt | integer |
| job_err_cnt | integer |
| create_time | timestamp without time zone |
| update_time | timestamp without time zone |
| acc_type | character varying |
| row_state | character varying |

## Table: `tiot_scheduler_err`
| Column Name | Data Type |
| ----------- | --------- |
| topic | character varying |
| job_name | character varying |
| utct | timestamp without time zone |
| contents | jsonb |
| err_msg | character varying |
| create_time | timestamp without time zone |

