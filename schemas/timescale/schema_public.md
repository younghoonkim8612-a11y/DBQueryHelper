# Schema: public — Timescale DB (공통)
Updated: 2026-03-19

이 스키마는 모든 Timescale DB (Dev/Prod/기타 프로젝트)에 공통 적용됩니다.
프로젝트별로 테이블이 추가/제거될 수 있으나 기본 구조는 동일합니다.

### public.device_event
| Column | Type | Nullable |
|--------|------|----------|
| deid | character varying | NO |
| teid | character varying | YES |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| type | character varying | NO |
| evt_cd | character varying | NO |
| evt_dtl | character varying | YES |
| contents | jsonb | YES |
| create_time | timestamp without time zone | NO |

### public.msg_bi_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_edge_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_eq_agg_5min
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| eqty | character varying | YES |
| cons | bigint | YES |
| dist | bigint | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| create_time | timestamp without time zone | NO |

### public.msg_eq_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_event_history
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

**type/eqty별 contents (jsonb) 구조:**

type=`TIOT`, eqty=`QC` — QC 장비 이력 (MEID별 Body 구조가 다름):

MEID=`2100` — QC 터미널 운영 상태:
```json
{ "MEID": "2100", "SEQN": 4, "UTCT": "...", "HIST_UTCT": "...",
  "Body": { "TURO": "터미널 운영 상태 (1=운영중)" } }
```

MEID=`2101` — QC 터미널 운영 플래그:
```json
{ "MEID": "2101", "SEQN": 3, "UTCT": "...", "HIST_UTCT": "...",
  "Body": { "TURF": "터미널 운영 플래그 (1=운영중)" } }
```

MEID=`2104` — QC 센서/스프레더 데이터:
```json
{ "MEID": "2104", "SEQN": 0, "UTCT": "...", "HIST_UTCT": "...", "UTCT_ORG": "...",
  "Body": {
    "LATI": "위도", "LONG": "경도",
    "HOIP": "호이스트 위치 (integer)", "PICK": "픽업 상태 (0/1)",
    "SPLD": "스프레더 로드 (0/1)", "SPRS": "스프레더 크기",
    "TANF": "트롤리 각도", "TLOC": "트롤리 위치",
    "TORQ": "토크", "TROP": "트롤리 운전", "WEIC": "중량"
  } }
```

MEID=`2106`/`3106` — QC 에러/경고:
```json
{ "MEID": "2106", "SEQN": 1, "UTCT": "...", "HIST_UTCT": "...", "UTCT_ORG": "...",
  "Body": {
    "ECOD": "이벤트 코드 (E004/E005=에러, W001=경고)",
    "ECST": "이벤트 상태 (0=해제, 1=발생)"
  } }
```

type=`RTLS`, eqty=`YT` — YT(야드 트랙터) RTLS 이력:
```json
{
  "MEID": "장비 ID",
  "SEQN": "시퀀스 번호",
  "HSEQ": "이력 시퀀스 (integer, optional)",
  "UTCT": "이벤트 발생 UTC",
  "HIST_UTCT": "이력 기록 UTC",
  "UTCT_ORG": "원본 UTC (밀리초, optional)",
  "Body": {
    "ECOD": "이벤트 코드 (W001=경고 등, optional)",
    "ECST": "이벤트 상태 (0=해제, 1=발생, optional)",
    "PRMR": "프라이머리 상태 (0/1, optional)",
    "TURF": "터미널 운영 플래그 (1=운영중, optional)"
  }
}
```

type=`RTLS`, eqty=`FLT` — FLT(지게차) RTLS 이력:
```json
{
  "MEID": "장비 ID",
  "SEQN": "시퀀스 번호",
  "HSEQ": "이력 시퀀스 (integer)",
  "UTCT": "이벤트 발생 UTC",
  "HIST_UTCT": "이력 기록 UTC",
  "Body": {
    "TURF": "터미널 운영 플래그 (1=운영중)"
  }
}
```
**JSONB 접근 예시:** `contents->'Body'->>'ECOD'` (이벤트코드), `contents->>'MEID'` (장비ID), `(contents->'Body'->>'ECST')::int` (이벤트상태)

### public.msg_gis_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_int_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_iris_error
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_job_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_periodic_armgc
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_periodic_history
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_periodic_qc
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_periodic_rtls
⚠️ 이 테이블에는 `time`, `rcvdt`, `timestamp` 같은 컬럼이 **없음**. 시간 필터링에는 반드시 `utct` 또는 `create_time`을 사용할 것.
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

**contents (jsonb) 구조:**
```json
{
  "MEID": "장비 ID (varchar)",
  "SEQN": "시퀀스 번호 (integer)",
  "UTCT": "UTC 타임스탬프 (yyMMdd HHmmss.SS) — ⚠️ 비정상 값 존재 (예: '0703150'처럼 자릿수 초과). to_timestamp 사용 시 반드시 길이 검증 필요: LENGTH(contents->>'UTCT') = 16",
  "Body": {
    "ALGS": "알고리즘 상태 (integer)",
    "BPDP": "브레이크 페달 위치 (integer, 999=미수신)",
    "CALS": "캘리브레이션 상태 (integer)",
    "DIRE": "주행 방향 (varchar, F=전진/R=후진)",
    "ENGH": "엔진 시간 누적 (numeric, 999=미수신)",
    "ENGT": "엔진 온도 (integer, 999=미수신)",
    "ENOP": "엔진 오일 압력 (integer, 999=미수신)",
    "FUEL": "연료 잔량 (integer, 999=미수신)",
    "GDIR": "GPS 방향/각도 (integer, 0-360, 999=미수신)",
    "GMOD": "GPS 모드 (varchar, 0=무효/1=유효)",
    "LATI": "위도 (varchar, WGS84)",
    "LONG": "경도 (varchar, WGS84)",
    "SBEL": "안전벨트 (integer, 999=미수신)",
    "SPED": "속도 (numeric)",
    "TFUE": "총 연료 소비량 (integer, 999=미수신)",
    "TIPR": "타이어 공기압 (integer, 999=미수신)",
    "VDHR": "차량 운행시간 누적 (integer, 999=미수신)"
  }
}
```
**참고:**
- 값이 `999`인 필드는 미수신/무효 데이터를 의미함.
- MEID 끝자리가 `2`인 데이터가 Periodic Message (위 구조). 앞자리는 장비마다 다름 (예: 7102, 3102 등).
- Body 내 필드는 장비에 따라 일부 추가/누락될 수 있음.
**JSONB 접근 예시:** `contents->'Body'->>'LATI'` (위도), `contents->>'MEID'` (장비ID)

### public.msg_periodic_rtls_all
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_tiot_alarm
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_tiot_delayed
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

**type별 contents (jsonb) 구조:**

type=`EDGE` — 엣지 디바이스 이벤트:
```json
{
  "MEID": "장비 ID",
  "UTCT": "UTC 타임스탬프 (yyMMdd HHmmss.SSS, optional)",
  "Body": {
    "PRMR": "프라이머리 상태 (0/1)",
    "TURF": "터미널 운영 플래그 (1=운영중, optional)"
  }
}
```

type=`PDS` — PDS 장비 위치/작업 이벤트:
```json
{
  "MCID": "장비 ID (e.g. RTG11)",
  "MCTP": "장비 유형 (e.g. RTG)",
  "BLCK": "블록 (e.g. E2)",
  "BAY": "베이 번호",
  "LCTP": "위치 타입 (Y=야드, TPL=작업위치)",
  "LANE": "레인 (optional)",
  "JBID": "작업 ID (optional)",
  "JBTP": "작업 유형 (DSCH=양하 등, optional)",
  "VTID": "차량 ID (optional)",
  "RCRT": "매칭 결과 (MATCH/NOTMATCH/ERROR, optional)"
}
```
또는 Body 래핑 형식: `{MEID, UTCT, Body: {BAY, BLCK, LCTP}}`

type=`TIOT` — IoT 장비 상세 이벤트 (주로 RTG/QC):
```json
{
  "MEID": "장비 ID",
  "SEQN": "시퀀스 번호 (integer)",
  "UTCT": "UTC 타임스탬프",
  "DWKT": "가동시간(초, integer)",
  "Body": {
    "BLCK": "블록", "BAY": "베이", "ROW": "열", "TIER": "단",
    "CODE": "상태코드 (PR01=작업중, PR03=대기 등)",
    "LATI": "위도", "LONG": "경도",
    "ORG_LATI": "원본 위도", "ORG_LONG": "원본 경도",
    "LCTP": "위치 타입 (Y=야드)",
    "HOIP": "호이스트 위치 (integer)",
    "PICK": "픽업 상태 (0/1)",
    "SPLD": "스프레더 로드 (0/1)",
    "SPRS": "스프레더 크기 (integer)",
    "TLOC": "트롤리 위치 (0/1)",
    "TORQ": "토크 (integer)",
    "TROP": "트롤리 운전 (integer)",
    "WEIC": "중량 (integer)",
    "JBID": "작업 ID (optional)",
    "LANE": "레인 (optional)"
  }
}
```

type=`adapter-pds` — PDS 어댑터 장비 위치 (간소화):
```json
{
  "MCID": "장비 ID (e.g. RTG01)",
  "MCTP": "장비 유형 (e.g. RTG)",
  "BLCK": "블록 (e.g. A1)",
  "BAY": "베이 번호",
  "LCTP": "위치 타입 (Y/N)",
  "JBID": "작업 ID (optional)",
  "JBTP": "작업 유형 (optional)",
  "RCRT": "매칭 결과 (optional)",
  "VTID": "차량 ID (optional)"
}
```

type=`RTLS` — RTLS 이벤트 (에러/펌웨어):
```json
{
  "MEID": "장비 ID",
  "UTCT": "UTC 타임스탬프",
  "DWKT": "가동시간(초, optional)",
  "SEQN": "시퀀스 번호 (optional)",
  "Body": {
    "ECOD": "이벤트 코드 (E001 등, optional)",
    "ECST": "이벤트 상태 (0=해제, 1=발생, optional)",
    "FWVE": "펌웨어 버전 (optional)"
  }
}
```

type=`ZODIAC` — TOS(ZODIAC) 컨테이너 이벤트:
```json
{
  "bizHeader": {
    "msgId": "메시지 ID", "action": "New/Update/Delete",
    "msgSeq": "메시지 시퀀스", "srcSys": "ZODIAC",
    "tmnlCd": "터미널 코드", "evtTime": "이벤트 시간"
  },
  "contents": [{
    "cntrNo": "컨테이너 번호", "cntrTp": "컨테이너 타입 (HC 등)",
    "cntrIso": "ISO 코드", "cntrWgt": "중량",
    "cntrCgoTp": "화물 타입 (GP 등)",
    "fe": "Full/Empty (F/E)", "cls": "클래스 (IB=인바운드)",
    "opr": "오퍼레이터", "pol": "적하항", "pod": "양하항",
    "location": {
      "blck": "블록", "bay": "베이", "row": "열", "tier": "단",
      "locTp": "위치타입 (Y=야드)", "blckTp": "블록타입 (STACK)"
    },
    "Reefer": {"setTemp": "설정온도", "currTemp": "현재온도", "plugSts": "플러그상태"}
  }]
}
```

type=`job-manager` — 작업 관리자 알람:
```json
{
  "MEID": "장비 ID",
  "UTCT": "UTC 타임스탬프",
  "Action": "Delete/Create",
  "Body": {
    "detectType": "ALARM",
    "almLvl": "WARNING/CRITICAL",
    "alarmOn": "true/false (boolean)",
    "latitude": "위도 (numeric)",
    "longitute": "경도 (numeric)",
    "eventTime": "이벤트 시간 (epoch ms)"
  }
}
```
**JSONB 접근 예시:** `contents->>'MCID'`, `contents->'Body'->>'ECOD'`, `contents->'bizHeader'->>'action'`

### public.msg_tiot_error
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_tiot_event
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_tos_in
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_tos_out
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.msg_vt_event
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| teid | character varying | NO |
| uidt | bigint | NO |
| utct | timestamp without time zone | NO |
| vers | character varying | NO |
| deid | character varying | YES |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| eqty | character varying | YES |
| create_time | timestamp without time zone | NO |

### public.qrtz_blob_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| blob_data | bytea | YES |

**Primary Key:** sched_name, trigger_name, trigger_group

**Foreign Keys:**
- sched_name → public.qrtz_triggers(sched_name)
- sched_name → public.qrtz_triggers(trigger_group)
- sched_name → public.qrtz_triggers(trigger_name)
- trigger_group → public.qrtz_triggers(sched_name)
- trigger_group → public.qrtz_triggers(trigger_group)
- trigger_group → public.qrtz_triggers(trigger_name)
- trigger_name → public.qrtz_triggers(sched_name)
- trigger_name → public.qrtz_triggers(trigger_group)
- trigger_name → public.qrtz_triggers(trigger_name)

### public.qrtz_calendars
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| calendar_name | character varying | NO |
| calendar | bytea | NO |

**Primary Key:** sched_name, calendar_name

### public.qrtz_cron_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| cron_expression | character varying | NO |
| time_zone_id | character varying | YES |

**Primary Key:** sched_name, trigger_name, trigger_group

**Foreign Keys:**
- sched_name → public.qrtz_triggers(sched_name)
- sched_name → public.qrtz_triggers(trigger_group)
- sched_name → public.qrtz_triggers(trigger_name)
- trigger_group → public.qrtz_triggers(sched_name)
- trigger_group → public.qrtz_triggers(trigger_group)
- trigger_group → public.qrtz_triggers(trigger_name)
- trigger_name → public.qrtz_triggers(sched_name)
- trigger_name → public.qrtz_triggers(trigger_group)
- trigger_name → public.qrtz_triggers(trigger_name)

### public.qrtz_fired_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| entry_id | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| instance_name | character varying | NO |
| fired_time | bigint | NO |
| sched_time | bigint | NO |
| priority | integer | NO |
| state | character varying | NO |
| job_name | character varying | YES |
| job_group | character varying | YES |
| is_nonconcurrent | boolean | YES |
| requests_recovery | boolean | YES |

**Primary Key:** sched_name, entry_id

### public.qrtz_job_details
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| job_name | character varying | NO |
| job_group | character varying | NO |
| description | character varying | YES |
| job_class_name | character varying | NO |
| is_durable | boolean | NO |
| is_nonconcurrent | boolean | NO |
| is_update_data | boolean | NO |
| requests_recovery | boolean | NO |
| job_data | bytea | YES |

**Primary Key:** sched_name, job_name, job_group

### public.qrtz_locks
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| lock_name | character varying | NO |

**Primary Key:** sched_name, lock_name

### public.qrtz_paused_trigger_grps
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_group | character varying | NO |

**Primary Key:** sched_name, trigger_group

### public.qrtz_scheduler_state
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| instance_name | character varying | NO |
| last_checkin_time | bigint | NO |
| checkin_interval | bigint | NO |

**Primary Key:** sched_name, instance_name

### public.qrtz_simple_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| repeat_count | bigint | NO |
| repeat_interval | bigint | NO |
| times_triggered | bigint | NO |

**Primary Key:** sched_name, trigger_name, trigger_group

**Foreign Keys:**
- sched_name → public.qrtz_triggers(sched_name)
- sched_name → public.qrtz_triggers(trigger_group)
- sched_name → public.qrtz_triggers(trigger_name)
- trigger_group → public.qrtz_triggers(sched_name)
- trigger_group → public.qrtz_triggers(trigger_group)
- trigger_group → public.qrtz_triggers(trigger_name)
- trigger_name → public.qrtz_triggers(sched_name)
- trigger_name → public.qrtz_triggers(trigger_group)
- trigger_name → public.qrtz_triggers(trigger_name)

### public.qrtz_simprop_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| str_prop_1 | character varying | YES |
| str_prop_2 | character varying | YES |
| str_prop_3 | character varying | YES |
| int_prop_1 | integer | YES |
| int_prop_2 | integer | YES |
| long_prop_1 | bigint | YES |
| long_prop_2 | bigint | YES |
| dec_prop_1 | numeric | YES |
| dec_prop_2 | numeric | YES |
| bool_prop_1 | boolean | YES |
| bool_prop_2 | boolean | YES |

**Primary Key:** sched_name, trigger_name, trigger_group

**Foreign Keys:**
- sched_name → public.qrtz_triggers(sched_name)
- sched_name → public.qrtz_triggers(trigger_group)
- sched_name → public.qrtz_triggers(trigger_name)
- trigger_group → public.qrtz_triggers(sched_name)
- trigger_group → public.qrtz_triggers(trigger_group)
- trigger_group → public.qrtz_triggers(trigger_name)
- trigger_name → public.qrtz_triggers(sched_name)
- trigger_name → public.qrtz_triggers(trigger_group)
- trigger_name → public.qrtz_triggers(trigger_name)

### public.qrtz_triggers
| Column | Type | Nullable |
|--------|------|----------|
| sched_name | character varying | NO |
| trigger_name | character varying | NO |
| trigger_group | character varying | NO |
| job_name | character varying | NO |
| job_group | character varying | NO |
| description | character varying | YES |
| next_fire_time | bigint | YES |
| prev_fire_time | bigint | YES |
| priority | integer | YES |
| trigger_state | character varying | NO |
| trigger_type | character varying | NO |
| start_time | bigint | NO |
| end_time | bigint | YES |
| calendar_name | character varying | YES |
| misfire_instr | smallint | YES |
| job_data | bytea | YES |

**Primary Key:** sched_name, trigger_name, trigger_group

**Foreign Keys:**
- job_group → public.qrtz_job_details(job_group)
- job_group → public.qrtz_job_details(job_name)
- job_group → public.qrtz_job_details(sched_name)
- job_name → public.qrtz_job_details(job_group)
- job_name → public.qrtz_job_details(job_name)
- job_name → public.qrtz_job_details(sched_name)
- sched_name → public.qrtz_job_details(job_group)
- sched_name → public.qrtz_job_details(job_name)
- sched_name → public.qrtz_job_details(sched_name)

### public.spatial_ref_sys
| Column | Type | Nullable |
|--------|------|----------|
| srid | integer | NO |
| auth_name | character varying | YES |
| auth_srid | integer | YES |
| srtext | character varying | YES |
| proj4text | character varying | YES |

**Primary Key:** srid

### public.temp_out_tml_rtg
| Column | Type | Nullable |
|--------|------|----------|
| teid | character varying | YES |
| eqty | character varying | YES |
| eqnm | character varying | YES |
| utct | timestamp without time zone | YES |
| body_utct | timestamp without time zone | YES |
| gmod | text | YES |
| geom | USER-DEFINED | YES |
| org_geom | USER-DEFINED | YES |

### public.tiot_border_status
| Column | Type | Nullable |
|--------|------|----------|
| job_date | character varying | NO |
| job_type | character varying | NO |
| job_detail | jsonb | YES |
| create_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |

### public.tiot_gis_tml
| Column | Type | Nullable |
|--------|------|----------|
| tml_id | text | YES |
| geom | USER-DEFINED | YES |

### public.tiot_itv_status
| Column | Type | Nullable |
|--------|------|----------|
| job_date | character varying | NO |
| job_type | character varying | YES |
| job_itv_no | character varying | YES |
| job_event | character varying | YES |
| job_detail | jsonb | YES |
| create_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |

### public.tiot_job_time_interval
| Column | Type | Nullable |
|--------|------|----------|
| job_interval_date | character varying | NO |
| job_interval_hour | character varying | NO |
| job_group_type | character varying | YES |
| job_group_no | character varying | YES |
| job_action_cnt | integer | YES |
| job_type_detail | jsonb | YES |
| create_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |

### public.tiot_job_time_interval_stat
| Column | Type | Nullable |
|--------|------|----------|
| job_interval_year | character varying | NO |
| job_interval_month | character varying | NO |
| job_interval_day | character varying | NO |
| job_group_type | character varying | YES |
| job_group_no | character varying | YES |
| job_action_cnt | integer | YES |
| job_type_detail | jsonb | YES |
| create_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |

### public.tiot_jobcycle
| Column | Type | Nullable |
|--------|------|----------|
| utct | timestamp without time zone | YES |
| cont_no | character varying | YES |
| start_time | character varying | YES |
| end_time | character varying | YES |
| job_total | jsonb | YES |
| job_detail | jsonb | YES |
| create_time | timestamp without time zone | YES |
| remake_yn | character varying | YES |

### public.tiot_kpi
| Column | Type | Nullable |
|--------|------|----------|
| id | integer | NO |
| teid | character varying | NO |
| tgrp | character varying | YES |
| eqnm | character varying | YES |
| eqty | character varying | YES |
| type | character varying | YES |
| contents | jsonb | NO |
| create_time | timestamp without time zone | YES |

### public.tiot_scheduler
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | NO |
| job_name | character varying | YES |
| start_utct | timestamp without time zone | YES |
| end_utct | timestamp without time zone | YES |
| job_limit_cnt | integer | YES |
| job_tot_cnt | integer | YES |
| job_suc_cnt | integer | YES |
| job_err_cnt | integer | YES |
| create_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |
| acc_type | character varying | YES |
| row_state | character varying | YES |

### public.tiot_scheduler_err
| Column | Type | Nullable |
|--------|------|----------|
| topic | character varying | YES |
| job_name | character varying | YES |
| utct | timestamp without time zone | YES |
| contents | jsonb | YES |
| err_msg | character varying | YES |
| create_time | timestamp without time zone | YES |

### public.uturn_detection
| Column | Type | Nullable |
|--------|------|----------|
| uturn_flag | boolean | YES |
| id | bigint | YES |
| eqnm | character varying | YES |
| pt | USER-DEFINED | YES |
| gps_time | timestamp with time zone | YES |
| gps_time_gap_sec | double precision | YES |
| speed | text | YES |
| heading | text | YES |
| angle_diff | integer | YES |
| angle_sum | bigint | YES |
| time_sum | double precision | YES |
| gmod | text | YES |
| create_time | timestamp without time zone | YES |
