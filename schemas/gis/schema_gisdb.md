# Schema: gisdb — GIS DB (공통)
Updated: 2026-03-19

이 스키마는 모든 GIS DB (Dev/Prod/프로젝트별)에 공통 적용됩니다.
스키마 이름은 프로젝트별로 다를 수 있음 (gisdb, gisdb_JED, gisdb_t2 등).
모든 geometry 컬럼은 WGS84 (SRID=4326). 표시 시 ST_AsText(geom) 사용.

## 프로젝트별 변형 참고
- **gisdb / gisdb_t2**: PK에 tml_id 포함 (composite key), FK 제약조건 있음, 대부분 NOT NULL
- **gisdb_JED**: PK에서 tml_id 제외 (단일 키), FK 제약조건 없음, 대부분 nullable
- **JED 전용 추가 테이블**: cam_map, pa_map, st_map, gfc_calibration_map_ddw

## FK 의존성 순서 (root → leaf)
tml_map/cog_grp → yrd_map/apr_map/htl_map/bld_map/... → bk_map → bay_map, bet_map → bit_map

### apr_map
| Column | Type | Nullable |
|--------|------|----------|
| apr_tml_id | character varying | NO |
| apr_apr_id | character varying | NO |
| geom | USER-DEFINED | NO |
| apr_apr_pv | character | NO |
| apr_cre_ui | character varying | NO |
| apr_cre_da | timestamp without time zone | NO |
| apr_upd_ui | character varying | NO |
| apr_upd_da | timestamp without time zone | NO |
| apr_apr_ds | character varying | NO |
| apr_apr_ar | double precision | NO |
| apr_apr_fm | character varying | YES |

**Primary Key:** apr_tml_id, apr_apr_id

**Foreign Keys:**
- apr_tml_id → tml_map(tml_tml_id)

### apr_map_history
| Column | Type | Nullable |
|--------|------|----------|
| apr_his_id | integer | NO |
| apr_tml_id | character varying | NO |
| apr_apr_id | character varying | NO |
| geom | USER-DEFINED | NO |
| apr_apr_pv | character | NO |
| apr_cre_ui | character varying | NO |
| apr_cre_da | timestamp without time zone | NO |
| apr_upd_ui | character varying | NO |
| apr_upd_da | timestamp without time zone | NO |
| apr_apr_ds | character varying | NO |
| apr_apr_ar | double precision | NO |
| apr_apr_fm | character varying | YES |

**Primary Key:** apr_his_id

### bay_map
| Column | Type | Nullable |
|--------|------|----------|
| bay_tml_id | character varying | NO |
| bay_bk_id | character varying | NO |
| bay_bay_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bay_bay_co | character varying | NO |
| bay_bay_rs | numeric | NO |
| bay_bay_tm | numeric | NO |
| bay_bay_td | numeric | NO |
| bay_bay_rl | character | YES |
| bay_cre_ui | character varying | NO |
| bay_cre_da | timestamp without time zone | NO |
| bay_upd_ui | character varying | NO |
| bay_upd_da | timestamp without time zone | NO |
| bay_bay_ds | character varying | NO |
| bay_bay_ar | double precision | NO |
| bay_bay_re | numeric | NO |
| bay_yrd_id | integer | NO |
| bay_bay_nm | character varying | NO |
| bay_bay_sn | character varying | NO |
| bay_bay_en | character varying | NO |

**Primary Key:** bay_tml_id, bay_yrd_id, bay_bk_id, bay_bay_id

**Foreign Keys:**
- bay_bk_id → bk_map(bk_bk_id)
- bay_bk_id → bk_map(bk_tml_id)
- bay_bk_id → bk_map(bk_yrd_id)
- bay_tml_id → bk_map(bk_bk_id)
- bay_tml_id → bk_map(bk_tml_id)
- bay_tml_id → bk_map(bk_yrd_id)
- bay_yrd_id → bk_map(bk_bk_id)
- bay_yrd_id → bk_map(bk_tml_id)
- bay_yrd_id → bk_map(bk_yrd_id)

### bay_map_history
| Column | Type | Nullable |
|--------|------|----------|
| bay_his_id | integer | NO |
| bay_tml_id | character varying | NO |
| bay_bk_id | character varying | NO |
| bay_bay_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bay_bay_co | character varying | NO |
| bay_bay_rs | numeric | NO |
| bay_bay_tm | numeric | NO |
| bay_bay_td | numeric | NO |
| bay_bay_rl | character | YES |
| bay_cre_ui | character varying | NO |
| bay_cre_da | timestamp without time zone | NO |
| bay_upd_ui | character varying | NO |
| bay_upd_da | timestamp without time zone | NO |
| bay_bay_ds | character varying | NO |
| bay_bay_ar | double precision | NO |
| bay_bay_re | numeric | NO |
| bay_yrd_id | integer | NO |
| bay_bay_nm | character varying | NO |
| bay_bay_sn | character varying | NO |
| bay_bay_en | character varying | NO |

**Primary Key:** bay_his_id

### bet_map
| Column | Type | Nullable |
|--------|------|----------|
| bet_tml_id | character varying | NO |
| bet_bet_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bet_bet_st | numeric | NO |
| bet_bet_en | numeric | NO |
| bet_cre_ui | character varying | NO |
| bet_cre_da | timestamp without time zone | NO |
| bet_upd_ui | character varying | NO |
| bet_upd_da | timestamp without time zone | NO |
| bet_bet_ds | character varying | NO |
| bet_bet_le | double precision | NO |
| bet_bet_an | numeric | YES |
| bet_apr_id | character varying | YES |
| bet_bet_fm | character varying | YES |

**Primary Key:** bet_tml_id, bet_bet_id

**Foreign Keys:**
- bet_apr_id → apr_map(apr_apr_id)
- bet_apr_id → apr_map(apr_tml_id)
- bet_tml_id → apr_map(apr_apr_id)
- bet_tml_id → apr_map(apr_tml_id)
- bet_tml_id → tml_map(tml_tml_id)

### bet_map_history
| Column | Type | Nullable |
|--------|------|----------|
| bet_his_id | integer | NO |
| bet_tml_id | character varying | NO |
| bet_bet_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bet_bet_st | numeric | NO |
| bet_bet_en | numeric | NO |
| bet_cre_ui | character varying | NO |
| bet_cre_da | timestamp without time zone | NO |
| bet_upd_ui | character varying | NO |
| bet_upd_da | timestamp without time zone | NO |
| bet_bet_ds | character varying | NO |
| bet_bet_le | double precision | NO |
| bet_bet_an | numeric | YES |
| bet_apr_id | character varying | YES |
| bet_bet_fm | character varying | YES |

**Primary Key:** bet_his_id

### bit_map
| Column | Type | Nullable |
|--------|------|----------|
| bit_tml_id | character varying | NO |
| bit_bet_id | character varying | NO |
| bit_bit_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bit_cre_ui | character varying | NO |
| bit_cre_da | timestamp without time zone | NO |
| bit_upd_ui | character varying | NO |
| bit_upd_da | timestamp without time zone | NO |
| bit_bit_ds | character varying | NO |
| bit_bit_ty | character | NO |

**Primary Key:** bit_tml_id, bit_bet_id, bit_bit_id

**Foreign Keys:**
- bit_bet_id → bet_map(bet_bet_id)
- bit_bet_id → bet_map(bet_tml_id)
- bit_tml_id → bet_map(bet_bet_id)
- bit_tml_id → bet_map(bet_tml_id)

### bit_map_history
| Column | Type | Nullable |
|--------|------|----------|
| bit_his_id | integer | NO |
| bit_tml_id | character varying | NO |
| bit_bet_id | character varying | NO |
| bit_bit_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bit_cre_ui | character varying | NO |
| bit_cre_da | timestamp without time zone | NO |
| bit_upd_ui | character varying | NO |
| bit_upd_da | timestamp without time zone | NO |
| bit_bit_ds | character varying | NO |
| bit_bit_ty | character | NO |

**Primary Key:** bit_his_id

### bk_map
| Column | Type | Nullable |
|--------|------|----------|
| bk_tml_id | character varying | NO |
| bk_yrd_id | integer | NO |
| bk_bk_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bk_bk_ty | character | YES |
| bk_bk_pv | character | YES |
| bk_bk_co | character | YES |
| bk_bk_bs | numeric | YES |
| bk_bk_be | numeric | YES |
| bk_bk_rw | numeric | YES |
| bk_bk_tm | numeric | YES |
| bk_bk_td | numeric | YES |
| bk_bk_bsd | character varying | YES |
| bk_bk_rsd | character varying | YES |
| bk_itv_dre | character varying | YES |
| bk_itv_drr | character varying | YES |
| bk_itv_drl | character | YES |
| bk_itv_bkd | character varying | YES |
| bk_otr_dre | character varying | YES |
| bk_otr_drr | character varying | YES |
| bk_otr_drl | character | YES |
| bk_otr_bkd | character varying | YES |
| bk_bk_rowd | character varying | YES |
| bk_bk_bmod | character | YES |
| bk_bk_pos | numeric | YES |
| bk_bk_svan | character varying | YES |
| bk_bk_ano | character varying | YES |
| bk_cre_ui | character varying | NO |
| bk_cre_da | timestamp without time zone | NO |
| bk_upd_ui | character varying | NO |
| bk_upd_da | timestamp without time zone | NO |
| bk_bk_ds | character varying | NO |
| bk_bk_ar | double precision | NO |
| bk_bk_nm | character varying | NO |
| bk_bk_fm | character varying | YES |

**Primary Key:** bk_tml_id, bk_yrd_id, bk_bk_id

**Foreign Keys:**
- bk_tml_id → yrd_map(yrd_tml_id)
- bk_tml_id → yrd_map(yrd_yrd_id)
- bk_yrd_id → yrd_map(yrd_tml_id)
- bk_yrd_id → yrd_map(yrd_yrd_id)

### bk_map_history
| Column | Type | Nullable |
|--------|------|----------|
| bk_his_id | integer | NO |
| bk_tml_id | character varying | NO |
| bk_yrd_id | integer | NO |
| bk_bk_id | character varying | NO |
| geom | USER-DEFINED | NO |
| bk_bk_ty | character | NO |
| bk_bk_pv | character | NO |
| bk_bk_co | character | NO |
| bk_bk_bs | numeric | NO |
| bk_bk_be | numeric | NO |
| bk_bk_rw | numeric | NO |
| bk_bk_tm | numeric | NO |
| bk_bk_td | numeric | NO |
| bk_bk_bsd | character varying | NO |
| bk_bk_rsd | character varying | NO |
| bk_itv_dre | character varying | NO |
| bk_itv_drr | character varying | NO |
| bk_itv_drl | character | NO |
| bk_itv_bkd | character varying | NO |
| bk_otr_dre | character varying | NO |
| bk_otr_drr | character varying | NO |
| bk_otr_drl | character | NO |
| bk_otr_bkd | character varying | NO |
| bk_bk_rowd | character varying | NO |
| bk_bk_bmod | character | NO |
| bk_bk_pos | numeric | YES |
| bk_bk_svan | character varying | NO |
| bk_bk_ano | character varying | NO |
| bk_cre_ui | character varying | NO |
| bk_cre_da | timestamp without time zone | NO |
| bk_upd_ui | character varying | NO |
| bk_upd_da | timestamp without time zone | NO |
| bk_bk_ds | character varying | NO |
| bk_bk_ar | double precision | NO |
| bk_bk_nm | character varying | NO |
| bk_bk_fm | character varying | YES |

**Primary Key:** bk_his_id

### bld_map
| Column | Type | Nullable |
|--------|------|----------|
| bld_tml_id | character varying | NO |
| bld_bld_id | integer | NO |
| geom | USER-DEFINED | NO |
| bld_bld_nm | character varying | NO |
| bld_bld_de | character varying | YES |
| bld_bld_ty | character varying | NO |
| bld_bld_fl | numeric | NO |
| bld_cre_ui | character varying | NO |
| bld_cre_da | timestamp without time zone | NO |
| bld_upd_ui | character varying | NO |
| bld_upd_da | timestamp without time zone | NO |
| bld_bld_ds | character varying | NO |
| bld_bld_ar | double precision | NO |

**Primary Key:** bld_tml_id, bld_bld_id

**Foreign Keys:**
- bld_tml_id → tml_map(tml_tml_id)

### bld_map_history
| Column | Type | Nullable |
|--------|------|----------|
| bld_his_id | integer | NO |
| bld_tml_id | character varying | NO |
| bld_bld_id | integer | NO |
| geom | USER-DEFINED | NO |
| bld_bld_nm | character varying | NO |
| bld_bld_de | character varying | YES |
| bld_bld_ty | character varying | NO |
| bld_bld_fl | numeric | NO |
| bld_cre_ui | character varying | NO |
| bld_cre_da | timestamp without time zone | NO |
| bld_upd_ui | character varying | NO |
| bld_upd_da | timestamp without time zone | NO |
| bld_bld_ds | character varying | NO |
| bld_bld_ar | double precision | NO |

**Primary Key:** bld_his_id

### cog_grp
| Column | Type | Nullable |
|--------|------|----------|
| cog_grp_id | character varying | NO |
| cog_grp_de | character varying | NO |
| cog_cre_ui | character varying | NO |
| cog_cre_da | timestamp without time zone | NO |
| cog_upd_ui | character varying | NO |
| cog_upd_da | timestamp without time zone | NO |

**Primary Key:** cog_grp_id

### cov_val
| Column | Type | Nullable |
|--------|------|----------|
| cov_grp_id | character varying | NO |
| cov_val_id | integer | NO |
| cov_val_cd | character varying | NO |
| cov_val_de | character varying | NO |
| cov_cre_ui | character varying | NO |
| cov_cre_da | timestamp without time zone | NO |
| cov_upd_ui | character varying | NO |
| cov_upd_da | timestamp without time zone | NO |

**Primary Key:** cov_val_id

**Foreign Keys:**
- cov_grp_id → cog_grp(cog_grp_id)

### fen_map
| Column | Type | Nullable |
|--------|------|----------|
| fen_tml_id | character varying | NO |
| fen_fen_id | integer | NO |
| geom | USER-DEFINED | NO |
| fen_fen_mt | character varying | NO |
| fen_fen_ht | numeric | NO |
| fen_cre_ui | character varying | NO |
| fen_cre_da | timestamp without time zone | NO |
| fen_upd_ui | character varying | NO |
| fen_upd_da | timestamp without time zone | NO |
| fen_fen_ds | character varying | NO |
| fen_fen_le | double precision | NO |

**Primary Key:** fen_tml_id, fen_fen_id

**Foreign Keys:**
- fen_tml_id → tml_map(tml_tml_id)

### fen_map_history
| Column | Type | Nullable |
|--------|------|----------|
| fen_his_id | integer | NO |
| fen_tml_id | character varying | NO |
| fen_fen_id | integer | NO |
| geom | USER-DEFINED | NO |
| fen_fen_mt | character varying | NO |
| fen_fen_ht | numeric | NO |
| fen_cre_ui | character varying | NO |
| fen_cre_da | timestamp without time zone | NO |
| fen_upd_ui | character varying | NO |
| fen_upd_da | timestamp without time zone | NO |
| fen_fen_ds | character varying | NO |
| fen_fen_le | double precision | NO |

**Primary Key:** fen_his_id

### gat_map
| Column | Type | Nullable |
|--------|------|----------|
| gat_tml_id | character varying | NO |
| gat_htl_id | integer | NO |
| gat_gat_id | integer | NO |
| geom | USER-DEFINED | NO |
| gat_gat_ty | character | NO |
| gat_gat_lc | numeric | NO |
| gat_cre_ui | character varying | NO |
| gat_cre_da | timestamp without time zone | NO |
| gat_upd_ui | character varying | NO |
| gat_upd_da | timestamp without time zone | NO |
| gat_gat_ds | character varying | NO |
| gat_gat_ar | double precision | NO |

**Primary Key:** gat_tml_id, gat_htl_id, gat_gat_id

**Foreign Keys:**
- gat_htl_id → htl_map(htl_htl_id)
- gat_htl_id → htl_map(htl_tml_id)
- gat_tml_id → htl_map(htl_htl_id)
- gat_tml_id → htl_map(htl_tml_id)

### gat_map_history
| Column | Type | Nullable |
|--------|------|----------|
| gat_his_id | integer | NO |
| gat_tml_id | character varying | NO |
| gat_htl_id | integer | NO |
| gat_gat_id | integer | NO |
| geom | USER-DEFINED | NO |
| gat_gat_ty | character | NO |
| gat_gat_lc | numeric | NO |
| gat_cre_ui | character varying | NO |
| gat_cre_da | timestamp without time zone | NO |
| gat_upd_ui | character varying | NO |
| gat_upd_da | timestamp without time zone | NO |
| gat_gat_ds | character varying | NO |
| gat_gat_ar | double precision | NO |

**Primary Key:** gat_his_id

### gco_tbl
| Column | Type | Nullable |
|--------|------|----------|
| gco_gfc_id | integer | NO |
| gco_gco_id | integer | NO |
| gco_gco_co | character varying | NO |
| gco_gco_sr | character varying | NO |
| gco_gco_tg | character varying | NO |
| gco_gco_at | character varying | YES |
| gco_gco_au | character varying | YES |
| gco_gco_av | numeric | YES |
| gco_cre_ui | character varying | NO |
| gco_cre_da | timestamp without time zone | NO |
| gco_upd_ui | character varying | NO |
| gco_upd_da | timestamp without time zone | NO |
| gco_tml_id | character varying | NO |

**Primary Key:** gco_tml_id, gco_gfc_id, gco_gco_id

**Foreign Keys:**
- gco_gfc_id → gfc_map(gfc_gfc_id)
- gco_gfc_id → gfc_map(gfc_tml_id)
- gco_tml_id → gfc_map(gfc_gfc_id)
- gco_tml_id → gfc_map(gfc_tml_id)

### gco_tbl_history
| Column | Type | Nullable |
|--------|------|----------|
| gco_his_id | integer | NO |
| gco_gfc_id | integer | NO |
| gco_gco_id | integer | NO |
| gco_gco_co | character varying | NO |
| gco_gco_sr | character varying | NO |
| gco_gco_tg | character varying | NO |
| gco_gco_at | character varying | YES |
| gco_gco_au | character varying | YES |
| gco_gco_av | numeric | YES |
| gco_cre_ui | character varying | NO |
| gco_cre_da | timestamp without time zone | NO |
| gco_upd_ui | character varying | NO |
| gco_upd_da | timestamp without time zone | NO |
| gco_tml_id | character varying | NO |

**Primary Key:** gco_his_id, gco_gco_id

### gfc_calibration_map
| Column | Type | Nullable |
|--------|------|----------|
| gfc_tml_id | character varying | NO |
| gfc_gfc_id | integer | NO |
| geom | USER-DEFINED | NO |
| gfc_gfc_nm | character varying | NO |
| gfc_gfc_tp | character varying | YES |
| gfc_gfc_st | character varying | YES |
| gfc_cre_ui | character varying | NO |
| gfc_cre_da | timestamp without time zone | NO |
| gfc_upd_ui | character varying | NO |
| gfc_upd_da | timestamp without time zone | NO |
| gfc_gfc_ds | character varying | NO |
| gfc_gfc_ar | double precision | NO |

**Primary Key:** gfc_tml_id, gfc_gfc_id

**Foreign Keys:**
- gfc_tml_id → tml_map(tml_tml_id)

### gfc_map
| Column | Type | Nullable |
|--------|------|----------|
| gfc_tml_id | character varying | NO |
| gfc_gfc_id | integer | NO |
| geom | USER-DEFINED | NO |
| gfc_gfc_nm | character varying | NO |
| gfc_cre_ui | character varying | NO |
| gfc_cre_da | timestamp without time zone | NO |
| gfc_upd_ui | character varying | NO |
| gfc_upd_da | timestamp without time zone | NO |
| gfc_gfc_ds | character varying | NO |
| gfc_gfc_ar | double precision | NO |
| gfc_gfc_tp | character varying | YES |

**Primary Key:** gfc_tml_id, gfc_gfc_id

**Foreign Keys:**
- gfc_tml_id → tml_map(tml_tml_id)

### gfc_map_history
| Column | Type | Nullable |
|--------|------|----------|
| gfc_his_id | integer | NO |
| gfc_tml_id | character varying | NO |
| gfc_gfc_id | integer | NO |
| geom | USER-DEFINED | NO |
| gfc_gfc_nm | character varying | NO |
| gfc_cre_ui | character varying | NO |
| gfc_cre_da | timestamp without time zone | NO |
| gfc_upd_ui | character varying | NO |
| gfc_upd_da | timestamp without time zone | NO |
| gfc_gfc_ds | character varying | NO |
| gfc_gfc_ar | double precision | NO |
| gfc_gfc_tp | character varying | YES |

**Primary Key:** gfc_his_id

### htl_map
| Column | Type | Nullable |
|--------|------|----------|
| htl_tml_id | character varying | NO |
| htl_htl_id | integer | NO |
| geom | USER-DEFINED | NO |
| htl_cre_ui | character varying | NO |
| htl_cre_da | timestamp without time zone | NO |
| htl_upd_ui | character varying | NO |
| htl_upd_da | timestamp without time zone | NO |
| htl_htl_ds | character varying | NO |
| htl_htl_ar | double precision | NO |

**Primary Key:** htl_tml_id, htl_htl_id

**Foreign Keys:**
- htl_tml_id → tml_map(tml_tml_id)

### htl_map_history
| Column | Type | Nullable |
|--------|------|----------|
| htl_his_id | integer | NO |
| htl_tml_id | character varying | NO |
| htl_htl_id | integer | NO |
| geom | USER-DEFINED | NO |
| htl_cre_ui | character varying | NO |
| htl_cre_da | timestamp without time zone | NO |
| htl_upd_ui | character varying | NO |
| htl_upd_da | timestamp without time zone | NO |
| htl_htl_ds | character varying | NO |
| htl_htl_ar | double precision | NO |

**Primary Key:** htl_his_id

### leg_map
| Column | Type | Nullable |
|--------|------|----------|
| leg_tml_id | character varying | NO |
| leg_leg_id | integer | NO |
| geom | USER-DEFINED | NO |
| leg_leg_fd | integer | YES |
| leg_leg_td | integer | YES |
| leg_leg_tg | character varying | YES |
| leg_leg_il | character varying | YES |
| leg_leg_ol | character varying | YES |
| leg_cre_ui | character varying | NO |
| leg_cre_da | timestamp without time zone | NO |
| leg_upd_ui | character varying | NO |
| leg_upd_da | timestamp without time zone | NO |
| leg_leg_ds | character varying | NO |
| leg_leg_le | double precision | NO |
| leg_leg_lc | character | NO |
| leg_leg_wt | double precision | YES |
| leg_leg_nm | character varying | YES |

**Primary Key:** leg_tml_id, leg_leg_id

**Foreign Keys:**
- leg_tml_id → tml_map(tml_tml_id)

### leg_map_history
| Column | Type | Nullable |
|--------|------|----------|
| leg_his_id | integer | NO |
| leg_tml_id | character varying | NO |
| geom | USER-DEFINED | NO |
| leg_leg_id | integer | NO |
| leg_leg_fd | integer | YES |
| leg_leg_td | integer | YES |
| leg_leg_tg | character varying | YES |
| leg_leg_il | character varying | YES |
| leg_leg_ol | character varying | YES |
| leg_cre_ui | character varying | NO |
| leg_cre_da | timestamp without time zone | NO |
| leg_upd_ui | character varying | NO |
| leg_upd_da | timestamp without time zone | NO |
| leg_leg_ds | character varying | NO |
| leg_leg_le | double precision | NO |
| leg_leg_lc | character | NO |
| leg_leg_nm | character varying | YES |

**Primary Key:** leg_his_id

### leg_map_vertices_pgr
| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| cnt | integer | YES |
| chk | integer | YES |
| ein | integer | YES |
| eout | integer | YES |
| the_geom | USER-DEFINED | YES |

**Primary Key:** id

### ltp_map
| Column | Type | Nullable |
|--------|------|----------|
| ltp_tml_id | character varying | NO |
| ltp_ltp_id | integer | NO |
| geom | USER-DEFINED | NO |
| ltp_cre_ui | character varying | NO |
| ltp_cre_da | timestamp without time zone | NO |
| ltp_upd_ui | character varying | NO |
| ltp_upd_da | timestamp without time zone | NO |
| ltp_ltp_ds | character varying | NO |
| ltp_ltp_ty | character | NO |
| ltp_ltp_an | numeric | NO |
| ltp_ltp_ht | numeric | NO |

**Primary Key:** ltp_tml_id, ltp_ltp_id

**Foreign Keys:**
- ltp_tml_id → tml_map(tml_tml_id)

### ltp_map_history
| Column | Type | Nullable |
|--------|------|----------|
| ltp_his_id | integer | NO |
| ltp_tml_id | character varying | NO |
| ltp_ltp_id | integer | NO |
| geom | USER-DEFINED | NO |
| ltp_cre_ui | character varying | NO |
| ltp_cre_da | timestamp without time zone | NO |
| ltp_upd_ui | character varying | NO |
| ltp_upd_da | timestamp without time zone | NO |
| ltp_ltp_ds | character varying | NO |
| ltp_ltp_ty | character | NO |
| ltp_ltp_an | numeric | NO |
| ltp_ltp_ht | numeric | NO |

**Primary Key:** ltp_his_id

### prk_map
| Column | Type | Nullable |
|--------|------|----------|
| prk_tml_id | character varying | NO |
| prk_prk_id | integer | NO |
| geom | USER-DEFINED | NO |
| prk_prk_nm | character varying | NO |
| prk_prk_de | character varying | YES |
| prk_prk_ty | character varying | NO |
| prk_cre_ui | character varying | NO |
| prk_cre_da | timestamp without time zone | NO |
| prk_upd_ui | character varying | NO |
| prk_upd_da | timestamp without time zone | NO |
| prk_prk_ds | character varying | NO |
| prk_prk_ar | double precision | NO |

**Primary Key:** prk_tml_id, prk_prk_id

**Foreign Keys:**
- prk_tml_id → tml_map(tml_tml_id)

### prk_map_history
| Column | Type | Nullable |
|--------|------|----------|
| prk_his_id | integer | NO |
| prk_tml_id | character varying | NO |
| prk_prk_id | integer | NO |
| geom | USER-DEFINED | NO |
| prk_prk_nm | character varying | NO |
| prk_prk_de | character varying | YES |
| prk_prk_ty | character varying | NO |
| prk_cre_ui | character varying | NO |
| prk_cre_da | timestamp without time zone | NO |
| prk_upd_ui | character varying | NO |
| prk_upd_da | timestamp without time zone | NO |
| prk_prk_ds | character varying | NO |
| prk_prk_ar | double precision | NO |

**Primary Key:** prk_his_id

### ral_map
| Column | Type | Nullable |
|--------|------|----------|
| ral_tml_id | character varying | NO |
| ral_ral_id | integer | NO |
| geom | USER-DEFINED | NO |
| ral_ral_ty | character | NO |
| ral_ral_wt | numeric | NO |
| ral_cre_ui | character varying | NO |
| ral_cre_da | timestamp without time zone | NO |
| ral_upd_ui | character varying | NO |
| ral_upd_da | timestamp without time zone | NO |
| ral_ral_ds | character varying | NO |
| ral_ral_le | double precision | NO |

**Primary Key:** ral_tml_id, ral_ral_id

**Foreign Keys:**
- ral_tml_id → tml_map(tml_tml_id)

### ral_map_history
| Column | Type | Nullable |
|--------|------|----------|
| ral_his_id | integer | NO |
| ral_tml_id | character varying | NO |
| ral_ral_id | integer | NO |
| geom | USER-DEFINED | NO |
| ral_ral_ty | character | NO |
| ral_ral_wt | numeric | NO |
| ral_cre_ui | character varying | NO |
| ral_cre_da | timestamp without time zone | NO |
| ral_upd_ui | character varying | NO |
| ral_upd_da | timestamp without time zone | NO |
| ral_ral_ds | character varying | NO |
| ral_ral_le | double precision | NO |

**Primary Key:** ral_his_id

### rcl_map
| Column | Type | Nullable |
|--------|------|----------|
| rcl_tml_id | character varying | NO |
| rcl_rcl_id | integer | NO |
| geom | USER-DEFINED | NO |
| rcl_rcl_nm | character varying | NO |
| rcl_rcl_cl | character varying | NO |
| rcl_rcl_tr | double precision | NO |
| rcl_rcl_rr | double precision | NO |
| rcl_rcl_lc | integer | NO |
| rcl_rcl_ow | character varying | NO |
| rcl_rcl_sl | bigint | NO |
| rcl_rcl_sn | integer | YES |
| rcl_rcl_tn | integer | YES |
| rcl_cre_ui | character varying | NO |
| rcl_cre_da | timestamp without time zone | NO |
| rcl_upd_ui | character varying | NO |
| rcl_upd_da | timestamp without time zone | NO |
| rcl_rcl_ds | character varying | NO |
| rcl_rcl_le | double precision | NO |
| rcl_rcl_rc | character | NO |

**Primary Key:** rcl_tml_id, rcl_rcl_id

**Foreign Keys:**
- rcl_tml_id → tml_map(tml_tml_id)

### rcl_map_history
| Column | Type | Nullable |
|--------|------|----------|
| rcl_his_id | integer | NO |
| rcl_tml_id | character varying | NO |
| rcl_rcl_id | integer | NO |
| geom | USER-DEFINED | NO |
| rcl_rcl_nm | character varying | NO |
| rcl_rcl_cl | character varying | NO |
| rcl_rcl_tr | double precision | NO |
| rcl_rcl_rr | double precision | NO |
| rcl_rcl_lc | integer | NO |
| rcl_rcl_ow | character varying | NO |
| rcl_rcl_sl | bigint | NO |
| rcl_rcl_sn | integer | YES |
| rcl_rcl_tn | integer | YES |
| rcl_cre_ui | character varying | NO |
| rcl_cre_da | timestamp without time zone | NO |
| rcl_upd_ui | character varying | NO |
| rcl_upd_da | timestamp without time zone | NO |
| rcl_rcl_ds | character varying | NO |
| rcl_rcl_le | double precision | NO |
| rcl_rcl_rc | character | NO |

**Primary Key:** rcl_his_id

### rcl_map_vertices_pgr
| Column | Type | Nullable |
|--------|------|----------|
| id | bigint | NO |
| cnt | integer | YES |
| chk | integer | YES |
| ein | integer | YES |
| eout | integer | YES |
| the_geom | USER-DEFINED | YES |

**Primary Key:** id

### rfi_map
| Column | Type | Nullable |
|--------|------|----------|
| rfi_tml_id | character varying | NO |
| rfi_rfi_id | integer | NO |
| geom | USER-DEFINED | NO |
| rfi_rfi_nm | character varying | NO |
| rfi_rfi_bn | character varying | NO |
| rfi_rfi_an | numeric | NO |
| rfi_rfi_du | character | NO |
| rfi_cre_ui | character varying | NO |
| rfi_cre_da | timestamp without time zone | NO |
| rfi_upd_ui | character varying | NO |
| rfi_upd_da | timestamp without time zone | NO |
| rfi_rfi_ds | character varying | NO |

**Primary Key:** rfi_tml_id, rfi_rfi_id

**Foreign Keys:**
- rfi_tml_id → tml_map(tml_tml_id)

### rfi_map_history
| Column | Type | Nullable |
|--------|------|----------|
| rfi_his_id | integer | NO |
| rfi_tml_id | character varying | NO |
| rfi_rfi_id | integer | NO |
| geom | USER-DEFINED | NO |
| rfi_rfi_nm | character varying | NO |
| rfi_rfi_bn | character varying | NO |
| rfi_rfi_an | numeric | NO |
| rfi_rfi_du | character | NO |
| rfi_cre_ui | character varying | NO |
| rfi_cre_da | timestamp without time zone | NO |
| rfi_upd_ui | character varying | NO |
| rfi_upd_da | timestamp without time zone | NO |
| rfi_rfi_ds | character varying | NO |

**Primary Key:** rfi_his_id

### rpg_map
| Column | Type | Nullable |
|--------|------|----------|
| rpg_tml_id | character varying | NO |
| rpg_rpg_id | integer | NO |
| geom | USER-DEFINED | NO |
| rpg_rpg_pv | character | NO |
| rpg_cre_ui | character varying | NO |
| rpg_cre_da | timestamp without time zone | NO |
| rpg_upd_ui | character varying | NO |
| rpg_upd_da | timestamp without time zone | NO |
| rpg_rpg_ds | character varying | NO |
| rpg_rpg_ar | double precision | NO |

**Primary Key:** rpg_tml_id, rpg_rpg_id

**Foreign Keys:**
- rpg_tml_id → tml_map(tml_tml_id)

### rpg_map_history
| Column | Type | Nullable |
|--------|------|----------|
| rpg_his_id | integer | NO |
| rpg_tml_id | character varying | NO |
| rpg_rpg_id | integer | NO |
| geom | USER-DEFINED | NO |
| rpg_rpg_pv | character | NO |
| rpg_cre_ui | character varying | NO |
| rpg_cre_da | timestamp without time zone | NO |
| rpg_upd_ui | character varying | NO |
| rpg_upd_da | timestamp without time zone | NO |
| rpg_rpg_ds | character varying | NO |
| rpg_rpg_ar | double precision | NO |

**Primary Key:** rpg_his_id

### tml_map
| Column | Type | Nullable |
|--------|------|----------|
| tml_tml_id | character varying | NO |
| geom | USER-DEFINED | NO |
| tml_tml_nm | character varying | NO |
| tml_tml_op | character | NO |
| tml_tml_ty | character | NO |
| tml_cre_ui | character varying | NO |
| tml_cre_da | timestamp without time zone | NO |
| tml_upd_ui | character varying | NO |
| tml_upd_da | timestamp without time zone | NO |
| tml_tml_ds | character varying | NO |
| tml_tml_ar | double precision | NO |

**Primary Key:** tml_tml_id

### tml_map_history
| Column | Type | Nullable |
|--------|------|----------|
| tml_his_id | integer | NO |
| tml_tml_id | character varying | NO |
| geom | USER-DEFINED | NO |
| tml_tml_nm | character varying | NO |
| tml_tml_op | character | NO |
| tml_tml_ty | character | NO |
| tml_cre_ui | character varying | NO |
| tml_cre_da | timestamp without time zone | NO |
| tml_upd_ui | character varying | NO |
| tml_upd_da | timestamp without time zone | NO |
| tml_tml_ds | character varying | NO |
| tml_tml_ar | double precision | NO |

**Primary Key:** tml_his_id

### yrd_map
| Column | Type | Nullable |
|--------|------|----------|
| yrd_tml_id | character varying | NO |
| yrd_yrd_id | integer | NO |
| geom | USER-DEFINED | NO |
| yrd_yrd_pv | character | NO |
| yrd_cre_ui | character varying | NO |
| yrd_cre_da | timestamp without time zone | NO |
| yrd_upd_ui | character varying | NO |
| yrd_upd_da | timestamp without time zone | NO |
| yrd_yrd_ds | character varying | NO |
| yrd_yrd_ar | double precision | NO |

**Primary Key:** yrd_tml_id, yrd_yrd_id

**Foreign Keys:**
- yrd_tml_id → tml_map(tml_tml_id)

### yrd_map_history
| Column | Type | Nullable |
|--------|------|----------|
| yrd_his_id | integer | NO |
| yrd_tml_id | character varying | NO |
| yrd_yrd_id | integer | NO |
| geom | USER-DEFINED | NO |
| yrd_yrd_pv | character | NO |
| yrd_cre_ui | character varying | NO |
| yrd_cre_da | timestamp without time zone | NO |
| yrd_upd_ui | character varying | NO |
| yrd_upd_da | timestamp without time zone | NO |
| yrd_yrd_ds | character varying | NO |
| yrd_yrd_ar | double precision | NO |

**Primary Key:** yrd_his_id

---
## JED 전용 테이블

아래 테이블은 JED 프로젝트에서만 존재합니다.

### cam_map (CCTV/카메라)
| Column | Type | Nullable |
|--------|------|----------|
| cam_cam_sn | integer | YES |
| cam_cam_dn | character varying | YES |
| cam_cam_nm | character varying | YES |
| cam_cam_md | character varying | YES |
| cam_cam_rs | character varying | YES |
| cam_cam_fl | character varying | YES |
| cam_cam_pn | character varying | YES |
| cam_cam_tl | character varying | YES |
| cam_cam_ar | character varying | YES |
| cam_cam_lc | character varying | YES |
| cam_cam_ht | character varying | YES |
| cam_cam_io | character varying | YES |
| cam_cam_au | character varying | YES |
| cam_cam_ip | character varying | YES |
| cam_cam_nc | character varying | YES |
| geom | USER-DEFINED | YES |
| cam_cam_rl | character varying | YES |
| cam_tml_id | character varying | YES |
| cam_cam_fv | integer | YES |
| cam_gm_cv | USER-DEFINED | YES |

### pa_map (PA 스피커)
| Column | Type | Nullable |
|--------|------|----------|
| geom | USER-DEFINED | YES |
| pa_pa_sn | character varying | YES |
| pa_pa_ar | character varying | YES |
| pa_pa_lc | character varying | YES |
| pa_pa_au | character varying | YES |
| pa_pa_ps | character varying | YES |
| pa_pa_io | character varying | YES |
| pa_pa_rl | character varying | YES |
| pa_tml_id | character varying | YES |
| pa_pa_tg | text | YES |
| pa_pa_nm | text | YES |
| pa_pa_ip | text | YES |
| pa_pa_ma | text | YES |
| pa_pa_ex | integer | YES |
| pa_pa_fv | integer | YES |
| pa_pa_ds | text | YES |
| pa_gm_cv | USER-DEFINED | YES |

### st_map (구역/층)
| Column | Type | Nullable |
|--------|------|----------|
| st_st_id | integer | YES |
| st_st_nm | character varying | YES |
| st_st_lv | integer | YES |
| st_ulv_id | integer | YES |
| geom | USER-DEFINED | YES |
| st_tml_id | character varying | YES |

### gfc_calibration_map_ddw (GFC 캘리브레이션 DDW)
| Column | Type | Nullable |
|--------|------|----------|
| gfc_tml_id | character varying | YES |
| gfc_gfc_id | integer | NO |
| geom | USER-DEFINED | YES |
| gfc_gfc_nm | character varying | YES |
| gfc_gfc_tp | character varying | YES |
| gfc_gfc_st | character varying | YES |
| gfc_cre_ui | character varying | YES |
| gfc_cre_da | timestamp without time zone | NO |
| gfc_upd_ui | character varying | YES |
| gfc_upd_da | timestamp without time zone | NO |
| gfc_gfc_ds | character varying | YES |
| gfc_gfc_ar | double precision | NO |
