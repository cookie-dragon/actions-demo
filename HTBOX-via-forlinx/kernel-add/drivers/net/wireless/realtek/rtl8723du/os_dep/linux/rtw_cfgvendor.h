/******************************************************************************
 *
 * Copyright(c) 2007 - 2017 Realtek Corporation.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of version 2 of the GNU General Public License as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 *
 *****************************************************************************/

#ifndef _RTW_CFGVENDOR_H_
#define _RTW_CFGVENDOR_H_

#define OUI_BRCM    0x001018
#define OUI_GOOGLE  0x001A11
#define BRCM_VENDOR_SUBCMD_PRIV_STR	1
#define ATTRIBUTE_U32_LEN                  (NLA_HDRLEN  + 4)
#define VENDOR_ID_OVERHEAD                 ATTRIBUTE_U32_LEN
#define VENDOR_SUBCMD_OVERHEAD             ATTRIBUTE_U32_LEN
#define VENDOR_DATA_OVERHEAD               (NLA_HDRLEN)

#define SCAN_RESULTS_COMPLETE_FLAG_LEN       ATTRIBUTE_U32_LEN
#define SCAN_INDEX_HDR_LEN                   (NLA_HDRLEN)
#define SCAN_ID_HDR_LEN                      ATTRIBUTE_U32_LEN
#define SCAN_FLAGS_HDR_LEN                   ATTRIBUTE_U32_LEN
#define GSCAN_NUM_RESULTS_HDR_LEN            ATTRIBUTE_U32_LEN
#define GSCAN_RESULTS_HDR_LEN                (NLA_HDRLEN)
#define GSCAN_BATCH_RESULT_HDR_LEN  (SCAN_INDEX_HDR_LEN + SCAN_ID_HDR_LEN + \
				     SCAN_FLAGS_HDR_LEN + \
				     GSCAN_NUM_RESULTS_HDR_LEN + \
				     GSCAN_RESULTS_HDR_LEN)

#define VENDOR_REPLY_OVERHEAD       (VENDOR_ID_OVERHEAD + \
				     VENDOR_SUBCMD_OVERHEAD + \
				     VENDOR_DATA_OVERHEAD)
typedef enum {
    /* don't use 0 as a valid subcommand */
    VENDOR_NL80211_SUBCMD_UNSPECIFIED,

    /* define all vendor startup commands between 0x0 and 0x0FFF */
    VENDOR_NL80211_SUBCMD_RANGE_START = 0x0001,
    VENDOR_NL80211_SUBCMD_RANGE_END   = 0x0FFF,

    /* define all GScan related commands between 0x1000 and 0x10FF */
    ANDROID_NL80211_SUBCMD_GSCAN_RANGE_START = 0x1000,
    ANDROID_NL80211_SUBCMD_GSCAN_RANGE_END   = 0x10FF,

    /* define all NearbyDiscovery related commands between 0x1100 and 0x11FF */
    ANDROID_NL80211_SUBCMD_NBD_RANGE_START = 0x1100,
    ANDROID_NL80211_SUBCMD_NBD_RANGE_END   = 0x11FF,

    /* define all RTT related commands between 0x1100 and 0x11FF */
    ANDROID_NL80211_SUBCMD_RTT_RANGE_START = 0x1100,
    ANDROID_NL80211_SUBCMD_RTT_RANGE_END   = 0x11FF,

    ANDROID_NL80211_SUBCMD_LSTATS_RANGE_START = 0x1200,
    ANDROID_NL80211_SUBCMD_LSTATS_RANGE_END   = 0x12FF,

    /* define all Logger related commands between 0x1400 and 0x14FF */
    ANDROID_NL80211_SUBCMD_DEBUG_RANGE_START = 0x1400,
    ANDROID_NL80211_SUBCMD_DEBUG_RANGE_END   = 0x14FF,

    /* define all wifi offload related commands between 0x1600 and 0x16FF */
    ANDROID_NL80211_SUBCMD_WIFI_OFFLOAD_RANGE_START = 0x1600,
    ANDROID_NL80211_SUBCMD_WIFI_OFFLOAD_RANGE_END   = 0x16FF,

    /* define all NAN related commands between 0x1700 and 0x17FF */
    ANDROID_NL80211_SUBCMD_NAN_RANGE_START = 0x1700,
    ANDROID_NL80211_SUBCMD_NAN_RANGE_END   = 0x17FF,

    /* define all Android Packet Filter related commands between 0x1800 and 0x18FF */
    ANDROID_NL80211_SUBCMD_PKT_FILTER_RANGE_START = 0x1800,
    ANDROID_NL80211_SUBCMD_PKT_FILTER_RANGE_END   = 0x18FF,

    /* This is reserved for future usage */

} ANDROID_VENDOR_SUB_COMMAND;

enum wl_vendor_subcmd {
    GSCAN_SUBCMD_GET_CAPABILITIES = ANDROID_NL80211_SUBCMD_GSCAN_RANGE_START,

    GSCAN_SUBCMD_SET_CONFIG,                            /* 0x1001 */

    GSCAN_SUBCMD_SET_SCAN_CONFIG,                       /* 0x1002 */
    GSCAN_SUBCMD_ENABLE_GSCAN,                          /* 0x1003 */
    GSCAN_SUBCMD_GET_SCAN_RESULTS,                      /* 0x1004 */
    GSCAN_SUBCMD_SCAN_RESULTS,                          /* 0x1005 */

    GSCAN_SUBCMD_SET_HOTLIST,                           /* 0x1006 */

    GSCAN_SUBCMD_SET_SIGNIFICANT_CHANGE_CONFIG,         /* 0x1007 */
    GSCAN_SUBCMD_ENABLE_FULL_SCAN_RESULTS,              /* 0x1008 */
    GSCAN_SUBCMD_GET_CHANNEL_LIST,                       /* 0x1009 */

    WIFI_SUBCMD_GET_FEATURE_SET,                         /* 0x100A */
    WIFI_SUBCMD_GET_FEATURE_SET_MATRIX,                  /* 0x100B */
    WIFI_SUBCMD_SET_PNO_RANDOM_MAC_OUI,                  /* 0x100C */
    WIFI_SUBCMD_NODFS_SET,                               /* 0x100D */
    WIFI_SUBCMD_SET_COUNTRY_CODE,                             /* 0x100E */
    /* Add more sub commands here */
    GSCAN_SUBCMD_SET_EPNO_SSID,                          /* 0x100F */

    WIFI_SUBCMD_SET_SSID_WHITE_LIST,                    /* 0x1010 */
    WIFI_SUBCMD_SET_ROAM_PARAMS,                        /* 0x1011 */
    WIFI_SUBCMD_ENABLE_LAZY_ROAM,                       /* 0x1012 */
    WIFI_SUBCMD_SET_BSSID_PREF,                         /* 0x1013 */
    WIFI_SUBCMD_SET_BSSID_BLACKLIST,                     /* 0x1014 */

    GSCAN_SUBCMD_ANQPO_CONFIG,                          /* 0x1015 */
    WIFI_SUBCMD_SET_RSSI_MONITOR,                       /* 0x1016 */
    WIFI_SUBCMD_CONFIG_ND_OFFLOAD,                      /* 0x1017 */
    /* Add more sub commands here */

    GSCAN_SUBCMD_MAX,

	RTT_SUBCMD_SET_CONFIG = ANDROID_NL80211_SUBCMD_RTT_RANGE_START,
	RTT_SUBCMD_CANCEL_CONFIG,
	RTT_SUBCMD_GETCAPABILITY,

    APF_SUBCMD_GET_CAPABILITIES = ANDROID_NL80211_SUBCMD_PKT_FILTER_RANGE_START,
    APF_SUBCMD_SET_FILTER,
};

enum gscan_attributes {
	GSCAN_ATTRIBUTE_NUM_BUCKETS = 10,
	GSCAN_ATTRIBUTE_BASE_PERIOD,
	GSCAN_ATTRIBUTE_BUCKETS_BAND,
	GSCAN_ATTRIBUTE_BUCKET_ID,
	GSCAN_ATTRIBUTE_BUCKET_PERIOD,
	GSCAN_ATTRIBUTE_BUCKET_NUM_CHANNELS,
	GSCAN_ATTRIBUTE_BUCKET_CHANNELS,
	GSCAN_ATTRIBUTE_NUM_AP_PER_SCAN,
	GSCAN_ATTRIBUTE_REPORT_THRESHOLD,
	GSCAN_ATTRIBUTE_NUM_SCANS_TO_CACHE,
	GSCAN_ATTRIBUTE_BAND = GSCAN_ATTRIBUTE_BUCKETS_BAND,

	GSCAN_ATTRIBUTE_ENABLE_FEATURE = 20,
	GSCAN_ATTRIBUTE_SCAN_RESULTS_COMPLETE,
	GSCAN_ATTRIBUTE_FLUSH_FEATURE,
	GSCAN_ATTRIBUTE_ENABLE_FULL_SCAN_RESULTS,
	GSCAN_ATTRIBUTE_REPORT_EVENTS,
	/* remaining reserved for additional attributes */
	GSCAN_ATTRIBUTE_NUM_OF_RESULTS = 30,
	GSCAN_ATTRIBUTE_FLUSH_RESULTS,
	GSCAN_ATTRIBUTE_SCAN_RESULTS,                       /* flat array of wifi_scan_result */
	GSCAN_ATTRIBUTE_SCAN_ID,                            /* indicates scan number */
	GSCAN_ATTRIBUTE_SCAN_FLAGS,                         /* indicates if scan was aborted */
	GSCAN_ATTRIBUTE_AP_FLAGS,                           /* flags on significant change event */
	GSCAN_ATTRIBUTE_NUM_CHANNELS,
	GSCAN_ATTRIBUTE_CHANNEL_LIST,

	/* remaining reserved for additional attributes */

	GSCAN_ATTRIBUTE_SSID = 40,
	GSCAN_ATTRIBUTE_BSSID,
	GSCAN_ATTRIBUTE_CHANNEL,
	GSCAN_ATTRIBUTE_RSSI,
	GSCAN_ATTRIBUTE_TIMESTAMP,
	GSCAN_ATTRIBUTE_RTT,
	GSCAN_ATTRIBUTE_RTTSD,

	/* remaining reserved for additional attributes */

	GSCAN_ATTRIBUTE_HOTLIST_BSSIDS = 50,
	GSCAN_ATTRIBUTE_RSSI_LOW,
	GSCAN_ATTRIBUTE_RSSI_HIGH,
	GSCAN_ATTRIBUTE_HOSTLIST_BSSID_ELEM,
	GSCAN_ATTRIBUTE_HOTLIST_FLUSH,

	/* remaining reserved for additional attributes */
	GSCAN_ATTRIBUTE_RSSI_SAMPLE_SIZE = 60,
	GSCAN_ATTRIBUTE_LOST_AP_SAMPLE_SIZE,
	GSCAN_ATTRIBUTE_MIN_BREACHING,
	GSCAN_ATTRIBUTE_SIGNIFICANT_CHANGE_BSSIDS,
	GSCAN_ATTRIBUTE_SIGNIFICANT_CHANGE_FLUSH,
	GSCAN_ATTRIBUTE_MAX
};

enum gscan_bucket_attributes {
	GSCAN_ATTRIBUTE_CH_BUCKET_1,
	GSCAN_ATTRIBUTE_CH_BUCKET_2,
	GSCAN_ATTRIBUTE_CH_BUCKET_3,
	GSCAN_ATTRIBUTE_CH_BUCKET_4,
	GSCAN_ATTRIBUTE_CH_BUCKET_5,
	GSCAN_ATTRIBUTE_CH_BUCKET_6,
	GSCAN_ATTRIBUTE_CH_BUCKET_7
};

enum gscan_ch_attributes {
	GSCAN_ATTRIBUTE_CH_ID_1,
	GSCAN_ATTRIBUTE_CH_ID_2,
	GSCAN_ATTRIBUTE_CH_ID_3,
	GSCAN_ATTRIBUTE_CH_ID_4,
	GSCAN_ATTRIBUTE_CH_ID_5,
	GSCAN_ATTRIBUTE_CH_ID_6,
	GSCAN_ATTRIBUTE_CH_ID_7
};

enum rtt_attributes {
	RTT_ATTRIBUTE_TARGET_CNT,
	RTT_ATTRIBUTE_TARGET_INFO,
	RTT_ATTRIBUTE_TARGET_MAC,
	RTT_ATTRIBUTE_TARGET_TYPE,
	RTT_ATTRIBUTE_TARGET_PEER,
	RTT_ATTRIBUTE_TARGET_CHAN,
	RTT_ATTRIBUTE_TARGET_MODE,
	RTT_ATTRIBUTE_TARGET_INTERVAL,
	RTT_ATTRIBUTE_TARGET_NUM_MEASUREMENT,
	RTT_ATTRIBUTE_TARGET_NUM_PKT,
	RTT_ATTRIBUTE_TARGET_NUM_RETRY
};

typedef enum wl_vendor_event {
    RTK_RESERVED1,
    RTK_RESERVED2,
    GSCAN_EVENT_SIGNIFICANT_CHANGE_RESULTS ,
    GSCAN_EVENT_HOTLIST_RESULTS_FOUND,
    GSCAN_EVENT_SCAN_RESULTS_AVAILABLE,
    GSCAN_EVENT_FULL_SCAN_RESULTS,
    RTT_EVENT_COMPLETE,
    GSCAN_EVENT_COMPLETE_SCAN,
    GSCAN_EVENT_HOTLIST_RESULTS_LOST,
    GSCAN_EVENT_EPNO_EVENT,
    GOOGLE_DEBUG_RING_EVENT,
    GOOGLE_DEBUG_MEM_DUMP_EVENT,
    GSCAN_EVENT_ANQPO_HOTSPOT_MATCH,
    GOOGLE_RSSI_MONITOR_EVENT
} wl_vendor_event_t;

enum andr_wifi_feature_set_attr {
	ANDR_WIFI_ATTRIBUTE_NUM_FEATURE_SET,
	ANDR_WIFI_ATTRIBUTE_FEATURE_SET
};

typedef enum wl_vendor_gscan_attribute {
	ATTR_START_GSCAN,
	ATTR_STOP_GSCAN,
	ATTR_SET_SCAN_BATCH_CFG_ID, /* set batch scan params */
	ATTR_SET_SCAN_GEOFENCE_CFG_ID, /* set list of bssids to track */
	ATTR_SET_SCAN_SIGNIFICANT_CFG_ID, /* set list of bssids, rssi threshold etc.. */
	ATTR_SET_SCAN_CFG_ID, /* set common scan config params here */
	ATTR_GET_GSCAN_CAPABILITIES_ID,
	/* Add more sub commands here */
	ATTR_GSCAN_MAX
} wl_vendor_gscan_attribute_t;

typedef enum gscan_batch_attribute {
	ATTR_GSCAN_BATCH_BESTN,
	ATTR_GSCAN_BATCH_MSCAN,
	ATTR_GSCAN_BATCH_BUFFER_THRESHOLD
} gscan_batch_attribute_t;

typedef enum gscan_geofence_attribute {
	ATTR_GSCAN_NUM_HOTLIST_BSSID,
	ATTR_GSCAN_HOTLIST_BSSID
} gscan_geofence_attribute_t;

typedef enum gscan_complete_event {
	WIFI_SCAN_BUFFER_FULL,
	WIFI_SCAN_COMPLETE
} gscan_complete_event_t;

/* Capture the BRCM_VENDOR_SUBCMD_PRIV_STRINGS* here */
#define BRCM_VENDOR_SCMD_CAPA	"cap"

#if (LINUX_VERSION_CODE >= KERNEL_VERSION(3, 14, 0)) || defined(RTW_VENDOR_EXT_SUPPORT)
extern int rtw_cfgvendor_attach(struct wiphy *wiphy);
extern int rtw_cfgvendor_detach(struct wiphy *wiphy);
extern int rtw_cfgvendor_send_async_event(struct wiphy *wiphy,
	struct net_device *dev, int event_id, const void  *data, int len);
#if defined(GSCAN_SUPPORT) && 0
extern int wl_cfgvendor_send_hotlist_event(struct wiphy *wiphy,
	struct net_device *dev, void  *data, int len, wl_vendor_event_t event);
#endif
#endif /* (LINUX_VERSION_CODE >= KERNEL_VERSION(3, 14, 0)) || defined(RTW_VENDOR_EXT_SUPPORT) */

#endif /* _RTW_CFGVENDOR_H_ */
