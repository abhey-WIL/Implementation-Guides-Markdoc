---
title: EV Charging – General Implementation Guide
---

# EV Charging – General Implementation Guide

This guide is composed from the canonical EV Charging implementation guide
maintained in the `beckn/DEG` repository, plus additional commentary and
examples intended for general public use.

---

# 1. Request for Comments


# 2. Copyright Notice

**License: [CC-BY-NC-SA 4.0](https://becknprotocol.io/license/) becknprotocol.io**


# 3. Status of This Memo

**This is a draft RFC for implementing EV charging use cases using the Beckn Protocol. It provides implementation guidance for anyone to build interoperable EV charging applications that integrate with each other on a decentralized network while maintaining compatibility with OCPI standards for CPO communication.**


# 4. Abstract

This document proposes a practical way to make EV charging services easier to find and use by applying the Beckn Protocol’s distributed commerce model. Instead of juggling multiple apps and accounts for different charging networks, EV users on any Beckn protocol-enabled consumer platform (a.k.a BAPs) – can discover and book charging services from Beckn protocol-enabled provider platforms (a.k.a BPPs) that have onboarded one or more Charge Point Operators (CPOs).

EV users can discover, compare options, view transparent pricing, and reserve a slot at any eligible charging station owned or operated by CPOs. By standardizing discovery, pricing, and booking, the approach tackles three persistent barriers to EV adoption: charging anxiety, network fragmentation, and payment complexity.

Built on Beckn’s commerce capabilities and aligned with OCPI for technical interoperability, the implementation lets e-Mobility Service Providers (eMSPs) aggregate services from multiple CPOs while delivering a consistent, app-agnostic experience to consumers.


# 5. Introduction

This document provides an implementation guidance for deploying EV charging services using the Beckn Protocol ecosystem. It specifically addresses how consumer applications can provide unified access to charging infrastructure across multiple Charge Point Operators while maintaining technical compatibility with existing OCPI-based systems.


# 6. Scope

This document covers:

* Architecture patterns for EV charging marketplace implementation using Beckn Protocol  
* Discovery and charging mechanisms for charging EVs across multiple CPOs  
* Some recommendations for BAPs, BPPs and NFOs on how to map protocol API calls to internal systems (or vice-versa).  
* Real-time availability and pricing integration with OCPI-based systems  
* Session management and billing coordination between Beckn and OCPI protocols

This document does NOT cover:

* Detailed OCPI protocol specifications (refer to OCPI 2.2.1 documentation)  
* Physical charging infrastructure requirements and standards  
* Regulatory compliance beyond technical implementation (varies by jurisdiction)  
* Smart grid integration and load management systems


# 7. Intended Audience

* Consumer Application Developers (BAPs): Building EV driver-facing charging applications with unified cross-network access  
* e-Mobility Service Providers (eMSPs/BPPs): Implementing charging service aggregation platforms across multiple CPO networks  
* Charge Point Operators (CPOs): Understanding integration requirements for Beckn-enabled marketplace participation  
* Technology Integrators: Building bridges between existing OCPI infrastructure and new Beckn-based marketplaces  
* System Architects: Designing scalable, interoperable EV charging ecosystems  
* Business Stakeholders: Understanding technical capabilities and implementation requirements for EV charging marketplace strategies  
* Standards Organizations: Evaluating interoperability approaches for future EV charging standards development


# 8. Conventions and Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](https://github.com/beckn/protocol-specifications/blob/draft/docs/BECKN-010-Keyword-Definitions-for-Technical-Specifications.md).


# 9. Terminology

| Acronym | Full Form/Description             | Description                                                                                                           |
| ------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| BAP     | Beckn Application Platform        | Consumer-facing application that initiates transactions. Mapped to EV users and eMSPs.                                |
| BPP     | Beckn Provider Platform           | Service provider platform that responds to BAP requests. Mapped to CPOs.                                              |
| NFO     | Network Facilitator Organization  | Organization responsible for the adoption and growth of the network. Usually the custodian of the network’s registry. |
| CDS     | Catalog Discovery Service         | Enables discovery of charging services from BPPs in the network.                                                      |
| eMSP    | e-Mobility Service Provider       | Service provider that aggregates multiple CPOs. Generally onboarded by BAPs.                                          |
| CPO     | Charge Point Operator             | Entity that owns and operates charging infrastructure. Generally onboarded by BPPs.                                   |
| EVSE    | Electric Vehicle Supply Equipment | Individual charging station unit. Owned and operated by CPOs                                                          |
| OCPI    | Open Charge Point Interface       | Protocol for communication between eMSPs and CPOs.                                                                    |

> Note:
> This document does not detail the mapping between Beckn Protocol and OCPI. Please refer to [this](../../../../docs/implementation-guides/v1-EOS/DEG00x_Mapping-OCPI-and-Beckn-Protocol-for-EV-Charging-Interoperability.md) document for the same.
> BPPs are NOT aggregators. Any CPO that has implemented a Beckn Protocol endpoint is a BPP. 
> For all sense and purposes, CPOs are essentially BPPs and eMSPs are essentially BAPs.


# 10. Reference Architecture

The section defines the reference ecosystem architecture that is used for building this implementation guide. 

## 10.1. Architecture Diagram

![](../assets/beckn-one-deg-arch.png)

## 10.2. Actors

1. Beckn One Global Root Registry  
2. Beckn One Catalog Discovery Service  
3. Beckn Application Platforms  
4. Beckn Provider Platforms  
5. EV Charging Registry


# 11. Creating an Open Network for EV Charging

To create an open network for EV charging requires all the EV charging BAPs, BPPs, to be able to discover each other and become part of a common club. This club is manifested in the form of a Registry maintained by an NFO. 

## 11.1. Setting up a Registry

The NP Registry serves as the root of addressability and trust for all network participants. It maintains comprehensive details such as the participant’s globally unique identifier (ID), network address (Beckn API URL), public key, operational domains, and assigned role (e.g., BAP, BPP, CDS). In addition to managing participant registration, authentication, authorization, and permission control, the Registry oversees participant verification, activation, and overall lifecycle management, ensuring that only validated and authorized entities can operate within the network.

![](../assets/registry-arch.png)

You can publish your registries at [DeDi.global](https://publish.dedi.global/).

### 11.1.1. For a Network Participant

#### 11.1.1.1. Step 1 :  Claiming a Namespace

To get started, any platform that has implemented Beckn Protocol MUST create a globally unique namespace for themselves.   
All NPs (BAPs, BPPs, CDS’es) **MUST** register as a user on dedi.global and claim a unique namespace against their FQDN to become globally addressable. As part of the claiming process, the user must prove ownership of the namespace by verifying the ownership of their domain. Namespace would be at an organisation level. You can put your organisation name as the name of the namespace.

#### 11.1.1.2. Step 2 :  Setting up a Registry

Once the namespace is claimed, each NP **MUST** create a Beckn NP registry in the namespace to list their subscriber details. While creating the registry, the user **MUST** configure it with the [subscriber schema](https://gist.githubusercontent.com/nirmalnr/a6e5b17522169ecea4f3ccdd831af7e4/raw/7744f2542034db9675901b61b41c8228ea239074/beckn-subscriber-no-refs.schema.json). Example of a registry name can be `subscription-details`.

#### 11.1.1.3. Step 3 :  Publishing subscriber details

In the registry that is created, NPs **MUST** publish their subscription details including their ID, network endpoints, public keys, operational domains and assigned roles (BAP, BPP) as records.

*Detailed steps to create namespaces and registries in dedi.global can be found [here](https://github.com/dedi-global/docs/blob/0976607aabc6641d330a3d41a3bd89ab8790ea09/user-guides/namespace%20and%20registry%20creation.md).*

### 11.1.2. Step 4 :  Share details of the registry created with the Beckn One team

Once the registry is created and details are published, the namespace and the registry name of the newly created registry should be shared with the beckn one team.

### 11.1.3. For a Network facilitator organization

#### 11.1.3.1. Step 1 :  Claiming a Namespace

An NFO **MAY** register as a user on dedi.global and claim a unique namespace against their FQDN. As part of the claiming process, the user must prove ownership of that namespace by verifying the ownership of that domain. The NFO name can be set as the name of the namespace. 
*Note: A calibrated roll out of this infrastructure is planned and hence before it is open to the general public NFOs are advised to share their own domain and the domains of their NPs to the Beckn One team so that they can be whitelisted which will allow the NPs to verify the same using TXT records in their DNS.*

#### 11.1.3.2. Step 2 :  Setting up a Registry

Network facilitators **MAY** create registries under their own namespace using the [subscriber reference schema](https://gist.githubusercontent.com/nirmalnr/a6e5b17522169ecea4f3ccdd831af7e4/raw/b7cf8a47e6531ef22744b43e6305b8d8cc106e7b/beckn-subscriber-reference.schema.json) to point to either whole registries or records created by the NPs in their own namespaces.  Example of a registry name can be `subscription-details`.

#### 11.1.3.3. Step 3 :  Publishing subscriber details

In the registry that is created, NFOs **MAY** publish records which act as pointers to either whole registries or records created by the NPs records. The URL field in the record would be the lookup URL for a registry or a record as per DeDi protocol.

Example: For referencing another registry created by an NP, the record details created would be:

```json
{
  "url": "https://.dedi.global/dedi/lookup/example-company/subscription-details",
  "type": "Registry",
  "subscriber_id": "example-company.com"
}
```

Here `example-company` is the namespace of the NP, and all records added in the registry is referenced here. 

If only one record in the registry needs to be referenced, then the record details created would be:

```json
{
  "url": "https://.dedi.global/dedi/lookup/example-company/subscription-details/energy-bap",
  "type": "Record",
  "subscriber_id": "example-company.com"
}
```

Here `energy-bap` is the name of the record created by the NP in this registry. Only that record is referenced here.

*Detailed steps to create namespaces and registries in dedi.global can be found [here](https://github.com/dedi-global/docs/blob/0976607aabc6641d330a3d41a3bd89ab8790ea09/user-guides/namespace%20and%20registry%20creation.md).*

#### 11.1.3.4. Step 4 :  Share details of the registry created with the Beckn One team

Once the registry is created and details are published, the namespace and the registry name of the newly created registry should be shared with the beckn one team.

## 11.2. Setting up the Protocol Endpoints

This section contains instructions to set up and test the protocol stack for EV charging transactions. 

### 11.2.1. Installing Beckn ONIX

All NPs SHOULD install the Beckn ONIX adapter to quickly get set up and become Beckn Protocol compliant. Click [here](https://github.com/Beckn-One/beckn-onix?tab=readme-ov-file#automated-setup-recommended)) to learn how to set up Beckn ONIX.

### 11.2.2. Configuring Beckn ONIX for EV Charging Transactions

A detailed Configuration Guide is available [here](https://github.com/Beckn-One/beckn-onix/blob/main/CONFIG.md). A quick read of key concepts from the link is recommended.

Specifically, for EV Charging, please use the following configuration:
1. Configure dediregistry plugin instead of registry plugin. Read more [here](https://github.com/Beckn-One/beckn-onix/tree/main/pkg/plugin/implementation/dediregistry).
2. Start with using Simplekeymanager plugin during development, read more [here](https://github.com/Beckn-One/beckn-onix/tree/main/pkg/plugin/implementation/simplekeymanager). For production deployment, you may setup vault.
3. For routing calls to Catalog Discovery Service, refer to routing configuration [here](https://github.com/Beckn-One/beckn-onix/blob/main/config/local-simple-routing-BAPCaller.yaml).

### 11.2.3. 10.2.3 Performing a test EV charging transaction

Step 1 : Download the postman collection, from [here](/testnet/postman-collections/v2/EV_Charging/).

Step 2 : Run API calls

If you are a BAP

1. Configure the collection/environment variables to the newly installed Beckn ONIX adapter URL and other variables in the collection.
2. Select the discover example and hit send
3. You should see the EV charging service catalog response

If you are a BPP

1. Configure the collection/environment variables to the newly installed Beckn ONIX adapter URL and other variables in the collection.
2. Select the on_status example and hit send
3. You should see the response in your console


# 12. Implementing EV Charging Semantics on Beckn Protocol

This section contains recommendations and guidelines on how to implement EV Charging Services on Beckn Protocol enabled networks. To ensure global interoperability between actors of the EV charging network, the semantics of the EV charging industry need to be mapped to the core schema of Beckn Protocol. The below table summarizes key semantic mappings between the EV Charging Domain and Beckn Protocol domain.

## 12.1. Key Assumptions

- **Assumption 1 :** EV charging is treated as a service, not as a physical object.  
- **Assumption 2:** All CPOs have implemented OCPI interfaces 

Each entity in the charging lifecycle — the service, the commercial terms, and the usage instance — maps to a well-defined semantic concept, enabling platforms to exchange information in a standardized, machine-readable way.

## 12.2. Semantic Model

| EV Charging Domain Entity | Charging Example                                                                       |                                                    Semantically maps to                                                     |
| ------------------------- | -------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------: |
| Charging Service Listing  | “DC Fast-Charging (60 kW CCS2)”                                                        | [Item](https://github.com/beckn/protocol-specifications-new/tree/main/schema/EvChargingService/v1/attributes.yaml)  |
| Charging service          | “₹18 per kWh”, “₹150 per hour”, “₹999 monthly pass”, “Off-peak discount 2 AM–5 AM”     |  [Offer](https://github.com/beckn/protocol-specifications-new/tree/main/schema/EvChargingOffer/v1/attributes.yaml)  |
| Charging Session          | A specific booking or usage instance created when the user plugs in or reserves a slot | [Order](https://github.com/beckn/protocol-specifications-new/tree/main/schema/EvChargingSession/v1/attributes.yaml) |

## 12.3. Example Category Codes

The following section contains example category codes that can be 

Charger types

| Code      | What it means                                                                              |
| --------- | ------------------------------------------------------------------------------------------ |
| AC\_SLOW  | AC charge points in the “slow” band (≈ 3–7 kW).                                            |
| AC\_FAST  | AC “fast” public charging (≈ 7–22 kW; UK fast band 8–49 kW covers AC up to \~22 kW).       |
| DC\_FAST  | DC “rapid/fast” typically \~50–149 kW.                                                     |
| DC\_ULTRA | DC “ultra-rapid/ultra-fast”, ≥ 150 kW (also aligns with AFIR focus on ≥ 150 kW corridors). |

Connector types

| Code    | What it means                                                                           |
| ------- | --------------------------------------------------------------------------------------- |
| TYPE1   | Type 1 (SAE J1772) AC connector (North America/JP usage).                               |
| TYPE2   | Type 2 (IEC 62196-2) AC connector; EU standard.                                         |
| CCS2    | Combined Charging System “Combo 2” (IEC 62196 based) enabling high-power DC on Type 2\. |
| CHADEMO | CHAdeMO DC fast-charging standard.                                                      |
| GB\_T   | China’s GB/T charging standard (AC & DC).                                               |

Service types

| Code                     | What it means                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| GREEN\_ENERGY\_CERTIFIED | Flag that the site/session is supplied by verified green energy per catalog metadata (e.g., OCPI EnergyMix.is\_green\_energy). |
| GO\_EU                   | Energy backed by EU Guarantees of Origin (GOs).                                                                                |
| REGO\_UK                 | Energy backed by the UK Renewable Energy Guarantees of Origin (REGO) scheme.                                                   |
| I\_REC                   | Energy backed by I-REC certificates (international EACs).                                                                      |
| V2G\_ENABLED             | Charger/site supports bidirectional power transfer (V2G), e.g., per ISO 15118-20 implementations.                              |
| REMOTE\_START\_STOP      | Remote start/stop of sessions exposed via roaming interface (OCPI Commands module).                                            |


## 13. Example Workflows (EV User’s Perspective) {#13-example-workflows-ev-users-perspective}

## 13.1. User Story – 1 - Walk-In to a charging station without reservation
<span id="131-example-1---walk-in-to-a-charging-station-without-reservation"></span>
This section covers a walk-in case where users discover the charger using third-party apps, word of mouth, or Beckn API, and then drive to the location, plug in their EV and charge their vehicle.

### 13.1.1. Consumer User Journey
<span id="1311-consumer-user-journey"></span>
A sales manager, Arjun, drives an EV to client meetings. He's time-bound, cost-conscious, and prefers simple, scan-and-go experiences. Arjun arrives at a large dine-in restaurant for a one-hour client meeting. He notices a charging bay in the parking lot and decides to top up while he's inside.

**Discovery and Selection:**
Arjun opens his EV app, taps "Scan & Charge," and immediately scans the QR code on the charger unit. The app rapidly retrieves all critical charger details:
* Connector Type: CCS2
* Power Rating: 50 kW DC Fast Charger
* Live Status: Available
* Tariff: ₹18.00/kWh
* Active Offers: A Lunch-Hour Promo is highlighted, offering 10% off between 12:00 PM and 2:00 PM.

**Order and Authorization**
Arjun opts for a cost-based top-up to manage his budget effectively.
* **Session Selection:** Arjun selects a session limit of ₹450.00.
* **Review and Confirmation:** He reviews the session terms, which clearly state:
    * Rate: ₹18.00/kWh (with a 10% auto-applied discount expected during the session).
    * Idle Fee Window: 10 minutes grace period post-session completion to avoid surcharges.
    * Cancellation Rules: Free cancellation is allowed before physically plugging in and initiating charging.
* **Payment Authorization:** He confirms the order and chooses UPI for authorization. The app instantly processes an authorization hold of ₹450.00 on his account.
* **ID Generation:** The app instantly returns a unique Booking/Transaction ID for the confirmed session reservation.

**Fulfilment and Real-time Monitoring**
Arjun plugs the cable into his EV's charging port and initiates the session directly from the app before heading into his meeting.
* **Session Start:** The charging session begins, and since it is within the promotional time window, the Lunch-Hour Promo discount (10%) is automatically applied, setting the effective rate to ₹16.20/kWh.
* **Live Progress:** While Arjun is in his meeting, the app provides a live dashboard showing the session's progress:
    * Energy Delivered (kWh): Real-time consumption, increasing second-by-second.
    * Cost Consumed (₹): The monetary value spent, tracking towards the ₹450.00 limit.
    * Estimated Kilowatt-Hours Remaining: An estimation of how much more energy can be delivered within the cost limit.
* **Status Alerts:** Immediate notification if the session speed is derated or if charging is unexpectedly interrupted.

**Post-Fulfilment and Reconciliation**
The charging session will terminate when the ₹450.00 cost limit is reached, or if the vehicle's SOC reaches 100%, whichever occurs first.
* **Session Stop:** Upon reaching the cost limit, the charging session automatically ceases. A notification is sent to Arjun's phone reminding him to unplug his vehicle promptly.
* **Digital Summary:** Arjun immediately receives a digital invoice and a comprehensive session summary in his app, which details:
    * Total Energy Delivered (e.g., 27.78 kWh).
    * Discount Applied (10% on the total energy cost).
    * Final Billed Amount (₹450.00).
* **Automatic Reconciliation:** If the session is interrupted or stops before the full ₹450.00 is consumed (e.g., only ₹325.00 worth of energy was delivered), the system automatically reconciles the payment:
    * The system calculates the exact cost for the energy delivered (e.g., ₹325.00).
    * It initiates an automatic refund/adjustment (e.g., ₹125.00) from the initial ₹450.00 authorization hold back to Arjun's UPI source, ensuring he is billed only for the energy actually consumed.

#### 13.1.2. API Calls and Schema
<span id="1312-api-calls-and-schema"></span>
<span id="13121-action-discover"></span>
<span id="13122-action-on_discover"></span>
<span id="13123-action-select"></span>
<span id="13124-action-on_select"></span>
<span id="13125-action-init"></span>
<span id="13126-action-on_init"></span>
<span id="13127-131261-action-on_status"></span>
<span id="13128-action-confirm"></span>
<span id="13129-action-on_confirm"></span>
<span id="131210-action-status"></span>
<span id="131211-action-on_status"></span>
<span id="131212-action-update-start-charging"></span>
<span id="131213-action-on_update-start-charging"></span>
<span id="131214-action-status-charging-session-progress"></span>
<span id="131215-action-on_status"></span>
<span id="131216-async-action-on_status"></span>
<span id="131217-action-on_update-stop-charging"></span>
<span id="131218-async-action-on_update-stop-charging"></span>
<span id="131219-action-rating"></span>
<span id="131220-action-on_rating"></span>
<span id="131221-action-support"></span>
<span id="131222-action-on_support"></span>
*Note: The API calls and schema for walk-in charging are identical to the advance reservation use case with minor differences in timing and availability. Where sections reference Use Case 2, the same API structure, field definitions, and examples apply unless specifically noted otherwise.*

**13.1.2.1. action: discover**
**Method:** POST
**Use Cases:** Arjun scans QR code on charger using his BAP user app.
<details>
<summary><a href="../Example-schemas/01_discover/discovery-by-QR.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "app.example.com",
    "bap_uri": "https://app.example.com/bap",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "a1eabf26-29f5-4a01-9d4e-4c5c9d1a3d02",
    "timestamp": "2025-10-14T07:31:00Z",
    "ttl": "PT30S",
    "schema_context": [
      "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld"
    ]
  },
  "message": {
    "filters": {
      "type": "jsonpath",
      "expression": "$[?(@.beckn:id == 'IND*CPO1*cs-01*evse-01*connectorid-01')]"
    }
  },
  "error": {}
}
```
</details>

**13.1.2.2. action: on_discover**
**Method:** POST
**Use Cases:** The app receives the charger's details (connector, power rating, live status, tariff, any active time-bound offer).
<details>
<summary><a href="../Example-schemas/02_on_discover/specific-item-catalog.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_discover",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:05Z",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "a1eabf26-29f5-4a01-9d4e-4c5c9d1a3d02",
    "bap_id": "app.example.com",
    "bap_uri": "https://app.example.com/bap",
    "ttl": "PT30S",
    "bpp_id": "example-cds.com",
    "bpp_uri": "https://example-cds.com/pilot/cds/energy/v2"
  },
  "message": {
    "catalogs": [
      {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Catalog",
        "beckn:id": "catalog-ev-charging-001",
        "beckn:descriptor": {
          "@type": "beckn:Descriptor",
          "schema:name": "EV Charging Services Network",
          "beckn:shortDesc": "Comprehensive network of fast charging stations across Bengaluru"
        },
        "beckn:bppId": "bpp.ev-network.example.com",
        "beckn:bppUri": "https://bpp.ev-network.example.com/bpp",
        "beckn:items": [
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Item",
            "beckn:id": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "DC Fast Charger - CCS2 (60kW)",
              "beckn:shortDesc": "High-speed DC charging station with CCS2 connector",
              "beckn:longDesc": "Ultra-fast DC charging station supporting CCS2 connector type with 60kW maximum power output. Features advanced thermal management and smart charging capabilities."
            },
            "beckn:category": {
              "@type": "schema:CategoryCode",
              "schema:codeValue": "ev-charging",
              "schema:name": "EV Charging"
            },
            "beckn:availabilityWindow": [
              {
                "@type": "beckn:TimePeriod",
                "schema:startTime": "2026-01-04T08:00:00Z",
                "schema:endTime": "2026-01-04T20:00:00Z"
              }
            ],
            "beckn:rateable": true,
            "beckn:rating": {
              "@type": "beckn:Rating",
              "beckn:ratingValue": 4.5,
              "beckn:ratingCount": 128
            },
            "beckn:isActive": true,
            "beckn:provider": {
              "beckn:id": "ecopower-charging",
              "beckn:descriptor": {
                "@type": "beckn:Descriptor",
                "schema:name": "EcoPower Charging Pvt Ltd"
              }
            },
            "beckn:itemAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld",
              "@type": "ChargingService",
              "connectorType": "CCS2",
              "maxPowerKW": 60,
              "minPowerKW": 5,
              "reservationSupported": true,
              "chargingStation": {
                "id": "IN-ECO-BTM-STATION-01",
                "serviceLocation": {
                  "@type": "beckn:Location",
                  "geo": {
                    "type": "Point",
                    "coordinates": [
                      77.5946,
                      12.9716
                    ]
                  },
                  "address": {
                    "streetAddress": "EcoPower BTM Hub, 100 Ft Rd",
                    "addressLocality": "Bengaluru",
                    "addressRegion": "Karnataka",
                    "postalCode": "560076",
                    "addressCountry": "IN"
                  }
                }
              },
              "amenityFeature": [
                "RESTAURANT",
                "RESTROOM",
                "WI-FI"
              ],
              "evseId": "IN*ECO*BTM*01*CCS2*A",
              "parkingType": "Mall",
              "powerType": "DC",
              "connectorFormat": "CABLE",
              "chargingSpeed": "FAST",
              "vehicleType": "4-WHEELER"
            }
          }
        ],
        "beckn:offers": [
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "eco-charge-offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            },
            "beckn:validity": {
              "@type": "beckn:TimePeriod",
              "schema:startDate": "2025-10-10T00:00:00Z",
              "schema:endDate": "2026-04-10T23:59:59Z"
            },
            "beckn:acceptedPaymentMethod": [
              "UPI",
              "CREDIT_CARD"
            ],
            "beckn:offerAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingOffer/v1/context.jsonld",
              "@type": "ChargingOffer",
              "tariffModel": "PER_KWH",
              "idleFeePolicy": {
                "currency": "INR",
                "value": 2,
                "applicableQuantity": {
                  "unitCode": "MIN",
                  "unitText": "minutes",
                  "unitQuantity": 10
                }
              }
            },
            "beckn:provider": "GoGreen-charging"
          },
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "go-green-offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:price": {
              "currency": "INR",
              "value": 18.5,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            },
            "beckn:validity": {
              "@type": "beckn:TimePeriod",
              "schema:startDate": "2025-10-20T00:00:00Z",
              "schema:endDate": "2026-04-20T23:59:59Z"
            },
            "beckn:acceptedPaymentMethod": [
              "UPI",
              "CREDIT_CARD"
            ],
            "beckn:offerAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingOffer/v1/context.jsonld",
              "@type": "ChargingOffer",
              "tariffModel": "PER_KWH",
              "idleFeePolicy": {
                "currency": "INR",
                "value": 2,
                "applicableQuantity": {
                  "unitCode": "MIN",
                  "unitText": "minutes",
                  "unitQuantity": 10
                }
              }
            },
            "beckn:provider": "GoGreen-charging"
          }
        ]
      }
    ]
  },
  "error": {}
}
```
</details>

**13.1.2.3. action: select**
**Method:** POST
**Use Cases:** Arjun selects a service offering from the options he gets. He chooses a 100 INR top-up.
<details>
<summary><a href="../Example-schemas/03_select/ev-charging-select.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "select",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:00Z",
    "message_id": "bb9f86db-9a3d-4e9c-8c11-81c8f1a7b901",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "ecopower-charging",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5"
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:acceptedOffer": {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:provider": "ecopower-charging",
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            }
          }
        }
      ],
      "beckn:orderAttributes": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
        "@type": "ChargingSession",
        "buyerFinderFee": {
          "feeType": "PERCENTAGE",
          "feeValue": 2.5
        },
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.4. action: on_select**
**Method:** POST
**Use Cases:** Arjun receives estimated quotations for the selected service.
<details>
<summary><a href="../Example-schemas/04_on_select/ev-charging-on_select.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_select",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:05Z",
    "message_id": "bb9f86db-9a3d-4e9c-8c11-81c8f1a7b901",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "ecopower-charging",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/draft/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5"
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:acceptedOffer": {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:provider": "ecopower-charging",
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            }
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:orderAttributes": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
        "@type": "ChargingSession",
        "buyerFinderFee": {
          "feeType": "PERCENTAGE",
          "feeValue": 2.5
        },
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.5. action: init**
**Method:** POST
**Use Cases:** Arjun provides his billing information.
<details>
<summary><a href="../Example-schemas/05_init/ev-charging-init-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "init",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6743e9e2-4fb5-487c-92b7-13ba8018f176",
    "timestamp": "2025-01-27T10:00:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "INITIATED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012",
          "settlementAccounts": [
            {
              "beneficiaryId": "example-bap.com",
              "accountHolderName": "Example BAP Solutions Pvt Ltd",
              "accountNumber": "9876543210123",
              "ifscCode": "HDFC0009876",
              "bankName": "HDFC Bank",
              "vpa": "example-bap@paytm"
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

> **Note:** In a Beckn payment transaction, users interact with Beckn Application Platform (BAP) to transact with Beckn Provider Platform (BPP). The core Payment object schema captures the primary payment flow, but additional settlement account information is required for secondary fund transfers between parties.

The PaymentSettlement schema extends the Payment object with an array of settlement accounts, where each account specifies:

1.Beneficiary ID - identifies which party the funds are to be settled to - mention the coorresponding subcriber id name here.
2.Bank account details - account number, IFSC code, account holder name, bank name
3.Virtual Payment Address (VPA) - UPI ID for digital payments
4.Payment URL - URL for payment processing/redirection

**13.1.2.6. action: on_init**
**Method:** POST
**Use Cases:** Arjun receives the charging session terms (rate, idle fee window, cancellation rules, payment terms etc). He reviews the terms. He chooses UPI and authorizes payment.
<details>
<summary><a href="../Example-schemas/06_on_init/ev-charging-on_init-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_init",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6743e9e2-4fb5-487c-92b7-13ba8018f176",
    "timestamp": "2025-01-27T10:00:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:beneficiary": "BPP",
        "beckn:acceptedPaymentMethod": [
          "BANK_TRANSFER",
          "UPI",
          "WALLET"
        ],
        "beckn:paymentStatus": "INITIATED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012",
          "settlementAccounts": [
            {
              "beneficiaryId": "example-bap.com",
              "accountHolderName": "Example BAP Solutions Pvt Ltd",
              "accountNumber": "9876543210123",
              "ifscCode": "HDFC0009876",
              "bankName": "HDFC Bank",
              "vpa": "example-bap@paytm"
            },
            {
              "beneficiaryId": "example-bpp.com",
              "accountHolderName": "EcoPower Charging Solutions Pvt Ltd",
              "accountNumber": "1234567890123",
              "ifscCode": "HDFC0001234",
              "bankName": "HDFC Bank",
              "vpa": "ecopower@paytm"
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

> **Note:** UPI-Native Payment Architecture To ensure seamless user experiences and reduced operational complexity, the Unified Bharat E-Charge (UBC) ecosystem implements a direct, redirection-less UPI payment flow. In this model, when a user initiates a transaction, the BPP retrieves a dynamically generated UPI intent link from the CPO’s payment gateway and relays it to the client application. The user confirms payment via any UPI app, which pushes funds directly to the CPO’s merchant VPA. The payment gateway then verifies the credit in real-time with the UPI network and confirms the success to the BPP, enabling immediate booking authorization and faster, multi-cycle daily settlements without traditional gateway redirections

**13.1.2.6.1. action: on_status**
**Method:** POST
**Use Cases:** Application then receives a notification on the completed status of the payment for the charging session.
<details>
<summary><a href="../Example-schemas/06_on_status_1/ev-charging-on_status-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "d4da89d5-2e42-4c36-9139-7f5682d5f104",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "PENDING",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.7. action: confirm**
**Method:** POST
**Use Cases:** Arjun confirms the order.
<details>
<summary><a href="../Example-schemas/07_confirm/ev-charging-confirm.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "confirm",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "PENDING",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.8. action: on_confirm**
**Method:** POST
**Use Cases:** The application then returns a booking/transaction ID along with the other charging session details.
<details>
<summary><a href="../Example-schemas/08_00_on_confirm/ev-charging-on_confirm.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_confirm",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.8.1 action: status**
**Method:** POST
**Use Cases:** Arjun is asked to plug in the charger by the application.
<details>
<summary><a href="../Example-schemas/08_01_status/ev-charging-connector-status.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.8.2 action: on_status**
**Method:** POST
**Use Cases:** The application recieves a notification that the gun is successfully connected to the vehicle.
<details>
<summary><a href="../Example-schemas/08_02_on_status/ev-charging-connector-on_status.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING",
          "connectorStatus": "PREPARING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.9. action: update (start charging)**
**Method:** POST
**Use Cases:** Arjun plugs in and starts the session from the app.
<details>
<summary><a href="../Example-schemas/09_update/ev-charging-start-update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6bd7be5b-ac21-4a5c-a787-5ec6980317e6",
    "timestamp": "2025-01-27T10:15:00Z",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.10. action: on_update (start charging)**
**Method:** POST
**Use Cases:** Response for the charging session initiation.
<details>
<summary><a href="../Example-schemas/10_on_update/ev-charging-start-on_update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6bd7be5b-ac21-4a5c-a787-5ec6980317e6",
    "timestamp": "2025-01-27T10:15:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "ACTIVE",
          "connectorType": "CCS2",
          "maxPowerKW": 50
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.11. action: track (charging-session progress)**
**Method:** POST
**Use Cases:** Arjun requests to track the live status of the charging session. state of charge (how much charging has been done).
<details>
<summary><a href="../Example-schemas/11_track/ev-charging-track.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "track",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6ace310b-6440-4421-a2ed-b484c7548bd5",
    "timestamp": "2025-01-27T17:00:40.065Z",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ]
    }
  },
  "error": {}
}
```
</details>

**13.1.2.12. action: on_track**
**Method:** POST
**Use Cases:** Arjun receives the state of charge (how much charging has been done) of the vehicle.
<details>
<summary><a href="../Example-schemas/12_on_track/ev-charging-on_track.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_track",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6ace310b-6440-4421-a2ed-b484c7548bd5",
    "timestamp": "2025-01-27T17:00:40.065Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "trackingAction": {
          "@type": "beckn:TrackAction",
          "target": {
            "@type": "schema:EntryPoint",
            "url": "https://track.bluechargenet-aggregator.io/session/SESSION-9876543210"
          }
        },
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "ACTIVE",
          "chargingTelemetry": [
            {
              "eventTime": "2025-01-27T17:00:00Z",
              "metrics": [
                {
                  "name": "STATE_OF_CHARGE",
                  "value": 62.5,
                  "unitCode": "PERCENTAGE"
                },
                {
                  "name": "POWER",
                  "value": 18.4,
                  "unitCode": "KWH"
                },
                {
                  "name": "ENERGY",
                  "value": 10.2,
                  "unitCode": "KW"
                },
                {
                  "name": "VOLTAGE",
                  "value": 392,
                  "unitCode": "VLT"
                },
                {
                  "name": "CURRENT",
                  "value": 47.0,
                  "unitCode": "AMP"
                }
              ]
            },
            {
              "eventTime": "2025-01-27T17:05:00Z",
              "metrics": [
                {
                  "name": "STATE_OF_CHARGE",
                  "value": 65.0,
                  "unitCode": "PERCENTAGE"
                },
                {
                  "name": "POWER",
                  "value": 17.1,
                  "unitCode": "KWH"
                },
                {
                  "name": "ENERGY",
                  "value": 11.1,
                  "unitCode": "KW"
                },
                {
                  "name": "VOLTAGE",
                  "value": 388,
                  "unitCode": "VLT"
                },
                {
                  "name": "CURRENT",
                  "value": 44.2,
                  "unitCode": "AMP"
                }
              ]
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.13. async action: on_update (stop-charging)**
**Method:** POST
**Use Case:** For the paid amount the session stops (or notifies the EV user to unplug). He receives a digital invoice and session summary in-app. If anything went wrong (e.g., session interrupted, SOC reaches 100%, etc.), the app reconciles to bill only for energy delivered and issues any adjustment or refund automatically.
<details>
<summary><a href="../Example-schemas/14_02_on_update/ev-charging-completed-on_update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "32f67afe-3d8c-4faa-bc2e-93b0791dcb02",
    "timestamp": "2025-01-27T11:45:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "COMPLETED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "COMPLETED"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.1.2.14. action: rating**
**Method:** POST
**Use Cases:** Arjun provides rating for the charging session.
<details>
<summary><a href="../Example-schemas/15_rating/ev-charging-rating.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "rating",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "89ee20fe-b592-48b0-a5c5-e38f6b90e569",
    "timestamp": "2025-01-27T12:00:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "ratings": [
      {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:RatingInput",
        "id": "fulfillment-001",
        "ratingValue": 4,
        "bestRating": 5,
        "worstRating": 1,
        "category": "FULFILLMENT",
        "feedback": {
          "comments": "Excellent charging experience! The station was clean, easy to find, and the charging was fast and reliable. The staff was helpful and the payment process was smooth.",
          "tags": [
            "fast-charging",
            "easy-to-use",
            "clean-station",
            "helpful-staff",
            "smooth-payment"
          ]
        }
      }
    ]
  },
  "error": {}
}
```
</details>

**13.1.2.15. action: on_rating**
**Method:** POST
**Use Cases:** Arjun receives an achievement after providing a rating.
<details>
<summary><a href="../Example-schemas/16_on_rating/ev-charging-on_rating.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_rating",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "89ee20fe-b592-48b0-a5c5-e38f6b90e569",
    "timestamp": "2025-01-27T12:00:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "received": true,
    "feedbackForm": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Form",
      "url": "https://example-bpp.com/feedback/portal",
      "mime_type": "application/xml",
      "submission_id": "feedback-123e4567-e89b-12d3-a456-426614174000"
    }
  },
  "error": {}
}
```
</details>

**13.1.2.16. action: support**
**Method:** POST
**Use Cases:** Arjun reaches out for support.
<details>
<summary><a href="../Example-schemas/17_support/ev-charging-support.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "support",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "dee432d9-36c9-4146-ad21-2f5bcac9b6a9",
    "timestamp": "2025-01-27T12:15:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "refId": "order-ev-charging-001",
    "refType": "ORDER",
    "support": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:SupportInfo",
      "name": "Ravi Kumar",
      "phone": "+91-9876543210",
      "email": "ravi.kumar@example.com",
      "hours": "Mon\u2013Sun: 6:00 PM - 10:00 PM IST",
      "channels": [
        "PHONE",
        "WHATSAPP"
      ]
    }
  },
  "error": {}
}
```
</details>

**13.1.2.17. action: on_support**
**Method:** POST
**Use Cases:** Arjun receives a response to his support request.
<details>
<summary><a href="../Example-schemas/18_on_support/ev-charging-on_support.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_support",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "dee432d9-36c9-4146-ad21-2f5bcac9b6a9",
    "timestamp": "2025-01-27T12:15:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "support": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:SupportInfo",
      "name": "BlueCharge Support Team",
      "phone": "18001080",
      "email": "support@bluechargenet-aggregator.io",
      "url": "https://support.bluechargenet-aggregator.io/ticket/SUP-20250730-001",
      "hours": "Mon\u2013Sun 24/7 IST",
      "channels": [
        "PHONE",
        "EMAIL",
        "WEB",
        "CHAT"
      ]
    }
  },
  "error": {}
}
```
</details>


## 13.2. User Story – 2 - Reservation of an EV charging time slot
<span id="132-use-case-2--reservation-of-an-ev-charging-time-slot"></span>
This section covers advance reservation of a charging slot where users discover and book a charger before driving to the location.

### 13.2.1. Consumer User Journey
<span id="13201-context"></span>
<span id="13202-discovery"></span>
<span id="132021-adam-discovers-nearby-charging-services"></span>
<span id="13203-order-reservation"></span>
<span id="13204-fulfilment-session-start--tracking"></span>
<span id="13205-post-fulfilment"></span>
Aisha is driving her electric vehicle along the highway when she notices that her battery level is getting low. Using an EV Charging application (BAP), Aisha discovers nearby charging stations that are compatible with her vehicle. The application retrieves available slots and charger specifications from the available provider's (BPP). Aisha selects a preferred charger and books a slot through the application via Beckn APIs to avoid waiting on arrival.

**Discovery and Selection:**
Aisha opens her EV Charging BAP (powered by a Beckn-enabled discovery network). She filters for:
* **Connector Type:** CCS2
* **Location:** DC Fast chargers within 5 km
* **Amenities:** Restaurants or cafes
* **Tariff Model:** Per kWh

The app queries multiple charging providers and returns options showing:
* **ETA:** Estimated time from current location
* **Real-time Availability:** Status of slots
* **Tariff:** Cost per kWh
* **Active Offers:** Lunch-hour discounts (e.g., promotional pricing)

She compares them and selects "EcoPower Highway Hub – Mandya Food Court".

**Order and Reservation:**
Aisha taps "Reserve Slot" for the 12:45 PM – 1:15 PM window.
* **Session Review:** The app displays the session terms:
    * **Tariff:** ₹18 / kWh
    * **Grace Period:** 10 min post-session
    * **Idle Fee Policy:** ₹2/min after grace
    * **Cancellation Rules:** Free up to 15 min before
    * **Payment Options:** Hold, Pre-pay, Post-pay
* **Payment and Confirmation:** She pays ₹500 via her credit card. Upon confirmation of payment receipt, the provider returns a unique Reservation ID.

**Fulfilment and Real-time Monitoring:**
On arrival at the station, Aisha initiates "Start Charging" on her application.
* **Authentication:** The backend matches the request to her Reservation ID and instructs her to plug in the charging gun.
* **Session Start:** Once connected, charging begins.
* **Live Telemetry:** While she enjoys lunch, the app provides live tracking:
    * **Energy Dispensed:** kWh delivered
    * **Elapsed Time:** Duration of the session
    * **Running Cost:** Current bill amount (₹)
    * **Completion Estimate:** Time remaining until full/target

If she arrives a few minutes late, the charger holds the slot until the grace period expires.

**Post-Fulfilment and Reconciliation:**
Charging auto-stops when the requested amount (₹500) is reached or when she manually ends the session.
* **Session Stop:** The system terminates the power flow.
* **Digital Summary:** The system issues a digital invoice and reimburces back the amount to her account.
* **Feedback:** The app prompts for quick feedback:
    * Amenity rating (1–5)
    * Overall experience (1–5)
    * Optional text comments

Satisfied, Aisha resumes her trip with time to spare.

#### 13.2.2. API Calls and Schema
<span id="1321-api-calls-and-schema"></span>
<span id="13211-action-discover"></span>
<span id="132111-discovery-of-ev-charging-services-within-a-circular-boundary"></span>
<span id="132112-discovery-within-circle--connector-specs-as-filters"></span>
<span id="132113-discovery-within-circle--vehicle-specifications-as-filters"></span>
<span id="132114-discovery-of-services-offered-by-a-specific-cpo"></span>
<span id="132115-viewing-details-of-a-single-charging-station-by-its-item-identifier"></span>
<span id="132116-fetching-details-of-a-specific-charger-evse-on-site-by-its-evse-identifier"></span>
<span id="132117-discovering-chargers-in-a-specific-circular-area-a-specific-connector-type-and-availability-time-range"></span>
<span id="13212-action-on_discover"></span>
<span id="132121-offers-as-part-of-the-catalog"></span>
<span id="13213-action-select"></span>
<span id="13214-action-on_select"></span>
<span id="132141-surge-pricing"></span>
<span id="13215-action-init"></span>
<span id="13216-action-on_init"></span>
<span id="13217-action-on_status-payment"></span>
<span id="13218-action-confirm"></span>
<span id="13219-action-on_confirm"></span>
<span id="132110-action-update-start-charging"></span>
<span id="132111-action-on_update-start-charging"></span>
<span id="132112-action-status"></span>
<span id="132113-action-on_status"></span>
<span id="132114-asynchronous-action-on_status-temporary-connection-interruption"></span>
<span id="13211401-aundercharge-power-cut-mid-session"></span>
<span id="13211402-b-overcharge-charger-offline-to-cms-keeps-dispensing"></span>
<span id="132115-asynchronous-action-on_update-stop-charging"></span>
<span id="132116-synchronousasynchronous-on_update-stop-charging"></span>
<span id="132117-action-cancel"></span>
<span id="132118-action-on_cancel"></span>
<span id="132119-action-rating"></span>
<span id="132120-action-on_rating"></span>
<span id="132121-action-support"></span>
<span id="132122-action-on_support"></span>
<span id="1322-integrating-with-your-software"></span>
<span id="13221-integrating-the-bap"></span>
<span id="13222-integrating-the-bpp"></span>
> **Note:** The API calls and schema for reservation follow a similar flow to walk-in but include specific checks for availability and slot booking.*

**13.2.2.1. action: discover**
**Method:** POST
**Use Cases:** Aisha searches for chargers with specific filters (Location, Connector type and a time slot).
<details>
<summary><a href="../Example-schemas/01_discover/discovery-within-a-timerange.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "app.example.com",
    "bap_uri": "https://app.example.com/bap",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "a1eabf26-29f5-4a01-9d4e-4c5c9d1a3d02",
    "timestamp": "2025-10-14T07:31:00Z",
    "ttl": "PT30S",
    "schema_context": [
      "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld"
    ]
  },
  "message": {
    "filters": {
      "type": "jsonpath",
      "expression": "$[?(@.beckn:itemAttributes.vehicleType == '4-WHEELER' && @.beckn:itemAttributes.connectorType == 'CCS2' && @.beckn:availabilityWindow[?(@.schema:startTime <= '2026-01-04T20:00:00Z' && @.schema:endTime >= '2026-01-04T08:00:00Z')])]"
    },
    "spatial": [
      {
        "op": "s_dwithin",
        "targets": "$['beckn:itemAttributes.chargingStation.serviceLocation.geo']",
        "geometry": {
          "type": "Point",
          "coordinates": [
            77.59,
            12.94
          ]
        },
        "distanceMeters": 10000
      }
    ]
  },
  "error": {}
}
```
</details>

**13.2.2.2. action: on_discover**
**Method:** POST
**Use Cases:** The app receives a list of charging stations matching criteria, including ETA, availability, and active offers.
<details>
<summary><a href="../Example-schemas/02_on_discover/ev-charging-on_discover.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_discover",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:05Z",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "a1eabf26-29f5-4a01-9d4e-4c5c9d1a3d02",
    "bap_id": "app.example.com",
    "bap_uri": "https://app.example.com/bap",
    "ttl": "PT30S",
    "bpp_id": "example-cds.com",
    "bpp_uri": "https://example-cds.com/pilot/cds/energy/v2"
  },
  "message": {
    "catalogs": [
      {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Catalog",
        "beckn:id": "catalog-ev-charging-001",
        "beckn:descriptor": {
          "@type": "beckn:Descriptor",
          "schema:name": "EV Charging Services Network",
          "beckn:shortDesc": "Comprehensive network of fast charging stations across Bengaluru"
        },
        "beckn:bppId": "bpp.ev-network.example.com",
        "beckn:bppUri": "https://bpp.ev-network.example.com/bpp",
        "beckn:items": [
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Item",
            "beckn:id": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "DC Fast Charger - CCS2 (60kW)",
              "beckn:shortDesc": "High-speed DC charging station with CCS2 connector",
              "beckn:longDesc": "Ultra-fast DC charging station supporting CCS2 connector type with 60kW maximum power output. Features advanced thermal management and smart charging capabilities."
            },
            "beckn:category": {
              "@type": "schema:CategoryCode",
              "schema:codeValue": "ev-charging",
              "schema:name": "EV Charging"
            },
            "beckn:availabilityWindow": [
              {
                "@type": "beckn:TimePeriod",
                "schema:startTime": "2026-01-04T08:00:00Z",
                "schema:endTime": "2026-01-04T20:00:00Z"
              }
            ],
            "beckn:rateable": true,
            "beckn:rating": {
              "@type": "beckn:Rating",
              "beckn:ratingValue": 4.5,
              "beckn:ratingCount": 128
            },
            "beckn:isActive": true,
            "beckn:provider": {
              "beckn:id": "ecopower-charging",
              "beckn:descriptor": {
                "@type": "beckn:Descriptor",
                "schema:name": "EcoPower Charging Pvt Ltd"
              }
            },
            "beckn:itemAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld",
              "@type": "ChargingService",
              "connectorType": "CCS2",
              "maxPowerKW": 60,
              "minPowerKW": 5,
              "reservationSupported": true,
              "chargingStation": {
                "id": "IN-ECO-BTM-STATION-01",
                "serviceLocation": {
                  "@type": "beckn:Location",
                  "geo": {
                    "type": "Point",
                    "coordinates": [
                      77.5946,
                      12.9716
                    ]
                  },
                  "address": {
                    "streetAddress": "EcoPower BTM Hub, 100 Ft Rd",
                    "addressLocality": "Bengaluru",
                    "addressRegion": "Karnataka",
                    "postalCode": "560076",
                    "addressCountry": "IN"
                  }
                }
              },
              "amenityFeature": [
                "RESTAURANT",
                "RESTROOM",
                "WI-FI"
              ],
              "evseId": "IN*ECO*BTM*01*CCS2*A",
              "parkingType": "Mall",
              "powerType": "DC",
              "connectorFormat": "CABLE",
              "chargingSpeed": "FAST",
              "vehicleType": "4-WHEELER"
            }
          },
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Item",
            "beckn:id": "IND*greencharge-koramangala*cs-02*IN*GC*KOR*01*CCS2*A*CCS2-B",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "DC Fast Charger - CCS2 (120kW)",
              "beckn:shortDesc": "Ultra-fast DC charging station with CCS2 connector",
              "beckn:longDesc": "Ultra-fast DC charging station supporting CCS2 connector type with 120kW maximum power output. Features liquid cooling and advanced power management."
            },
            "beckn:category": {
              "@type": "schema:CategoryCode",
              "schema:codeValue": "ev-charging",
              "schema:name": "EV Charging"
            },
            "beckn:availabilityWindow": [
              {
                "@type": "beckn:TimePeriod",
                "schema:startTime": "2026-01-04T07:00:00Z",
                "schema:endTime": "2026-01-04T22:00:00Z"
              }
            ],
            "beckn:rateable": true,
            "beckn:rating": {
              "@type": "beckn:Rating",
              "beckn:ratingValue": 4.7,
              "beckn:ratingCount": 89
            },
            "beckn:isActive": true,
            "beckn:provider": {
              "beckn:id": "greencharge-koramangala",
              "beckn:descriptor": {
                "@type": "beckn:Descriptor",
                "schema:name": "GreenCharge Energy Solutions"
              }
            },
            "beckn:itemAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld",
              "@type": "ChargingService",
              "connectorType": "CCS2",
              "maxPowerKW": 120,
              "minPowerKW": 10,
              "reservationSupported": true,
              "chargingStation": {
                "id": "cs-02",
                "serviceLocation": {
                  "@type": "beckn:Location",
                  "geo": {
                    "type": "Point",
                    "coordinates": [
                      77.6104,
                      12.9153
                    ]
                  },
                  "address": {
                    "streetAddress": "GreenCharge Koramangala, 80 Ft Rd",
                    "addressLocality": "Bengaluru",
                    "addressRegion": "Karnataka",
                    "postalCode": "560034",
                    "addressCountry": "IN"
                  }
                }
              },
              "amenityFeature": [
                "RESTAURANT",
                "RESTROOM",
                "WI-FI",
                "PARKING"
              ],
              "evseId": "IN*GC*KOR*01*CCS2*A",
              "parkingType": "OffStreet",
              "powerType": "DC",
              "connectorFormat": "CABLE",
              "chargingSpeed": "ULTRAFAST",
              "vehicleType": "3-WHEELER"
            }
          },
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Item",
            "beckn:id": "IND*powergrid-indiranagar*cs-03*IN*PG*IND*01*TYPE2*A*TYPE2-A",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "AC Fast Charger - Type 2 (22kW)",
              "beckn:shortDesc": "AC fast charging station with Type 2 connector",
              "beckn:longDesc": "AC fast charging station supporting Type 2 connector type with 22kW maximum power output. Ideal for overnight charging and workplace charging."
            },
            "beckn:category": {
              "@type": "schema:CategoryCode",
              "schema:codeValue": "ev-charging",
              "schema:name": "EV Charging"
            },
            "beckn:availabilityWindow": [
              {
                "@type": "beckn:TimePeriod",
                "schema:startTime": "2026-01-04T09:00:00Z",
                "schema:endTime": "2026-01-04T18:00:00Z"
              }
            ],
            "beckn:rateable": true,
            "beckn:rating": {
              "@type": "beckn:Rating",
              "beckn:ratingValue": 4.3,
              "beckn:ratingCount": 156
            },
            "beckn:isActive": true,
            "beckn:provider": {
              "beckn:id": "powergrid-indiranagar",
              "beckn:descriptor": {
                "@type": "beckn:Descriptor",
                "schema:name": "PowerGrid Charging Solutions"
              }
            },
            "beckn:itemAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingService/v1/context.jsonld",
              "@type": "ChargingService",
              "connectorType": "Type2",
              "maxPowerKW": 22,
              "minPowerKW": 3,
              "reservationSupported": true,
              "chargingStation": {
                "id": "cs-03",
                "serviceLocation": {
                  "@type": "beckn:Location",
                  "geo": {
                    "type": "Point",
                    "coordinates": [
                      77.6254,
                      12.9716
                    ]
                  },
                  "address": {
                    "streetAddress": "PowerGrid Indiranagar, 100 Ft Rd",
                    "addressLocality": "Bengaluru",
                    "addressRegion": "Karnataka",
                    "postalCode": "560008",
                    "addressCountry": "IN"
                  }
                }
              },
              "amenityFeature": [
                "RESTROOM",
                "WI-FI",
                "PARKING"
              ],
              "evseId": "IN*PG*IND*01*TYPE2*A",
              "parkingType": "Office",
              "powerType": "AC_3_PHASE",
              "connectorFormat": "SOCKET",
              "chargingSpeed": "NORMAL",
              "vehicleType": "4-WHEELER"
            }
          }
        ],
        "beckn:offers": [
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            },
            "beckn:validity": {
              "@type": "beckn:TimePeriod",
              "schema:startDate": "2025-10-01T00:00:00Z",
              "schema:endDate": "2026-03-31T23:59:59Z"
            },
            "beckn:acceptedPaymentMethod": [
              "UPI",
              "CREDIT_CARD",
              "WALLET"
            ],
            "beckn:offerAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingOffer/v1/context.jsonld",
              "@type": "ChargingOffer",
              "tariffModel": "PER_KWH",
              "idleFeePolicy": {
                "currency": "INR",
                "value": 2,
                "applicableQuantity": {
                  "unitCode": "MIN",
                  "unitText": "minutes",
                  "unitQuantity": 10
                }
              }
            },
            "beckn:provider": "ecopower-charging"
          },
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-120kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 120kW"
            },
            "beckn:items": [
              "IND*greencharge-koramangala*cs-02*IN*GC*KOR*01*CCS2*A*CCS2-B"
            ],
            "beckn:price": {
              "currency": "INR",
              "value": 22.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            },
            "beckn:validity": {
              "@type": "beckn:TimePeriod",
              "schema:startDate": "2025-10-15T00:00:00Z",
              "schema:endDate": "2026-04-15T23:59:59Z"
            },
            "beckn:acceptedPaymentMethod": [
              "UPI",
              "CREDIT_CARD",
              "WALLET",
              "BANK_TRANSFER"
            ],
            "beckn:offerAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingOffer/v1/context.jsonld",
              "@type": "ChargingOffer",
              "tariffModel": "PER_KWH",
              "idleFeePolicy": {
                "currency": "INR",
                "value": 3,
                "applicableQuantity": {
                  "unitCode": "MIN",
                  "unitText": "minutes",
                  "unitQuantity": 15
                }
              }
            },
            "beckn:provider": "greencharge-koramangala"
          },
          {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-type2-22kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - Type 2 22kW"
            },
            "beckn:items": [
              "IND*powergrid-indiranagar*cs-03*IN*PG*IND*01*TYPE2*A*TYPE2-A"
            ],
            "beckn:price": {
              "currency": "INR",
              "value": 15.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            },
            "beckn:validity": {
              "@type": "beckn:TimePeriod",
              "schema:startDate": "2025-10-20T00:00:00Z",
              "schema:endDate": "2026-04-20T23:59:59Z"
            },
            "beckn:acceptedPaymentMethod": [
              "UPI",
              "CREDIT_CARD",
              "WALLET",
              "BANK_TRANSFER"
            ],
            "beckn:offerAttributes": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingOffer/v1/context.jsonld",
              "@type": "ChargingOffer",
              "tariffModel": "PER_KWH",
              "idleFeePolicy": {
                "currency": "INR",
                "value": 1,
                "applicableQuantity": {
                  "unitCode": "MIN",
                  "unitText": "minutes",
                  "unitQuantity": 30
                }
              }
            },
            "beckn:provider": "powergrid-indiranagar"
          }
        ]
      }
    ]
  },
  "error": {}
}
```
</details>

**13.2.2.3. action: select**
**Method:** POST
**Use Cases:** Aisha selects "EcoPower Highway Hub" and chooses a time slot (12:45–1:15 PM).
<details>
<summary><a href="../Example-schemas/03_select/ev-charging-on_select.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "select",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:00Z",
    "message_id": "bb9f86db-9a3d-4e9c-8c11-81c8f1a7b901",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "ecopower-charging",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5"
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:acceptedOffer": {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:provider": "ecopower-charging",
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            }
          }
        }
      ],
      "beckn:orderAttributes": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
        "@type": "ChargingSession",
        "buyerFinderFee": {
          "feeType": "PERCENTAGE",
          "feeValue": 2.5
        },
        "preferences": {
          "startTime": "2026-01-04T08:00:00Z",
          "endTime": "2026-01-04T20:00:00Z"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.4. action: on_select**
**Method:** POST
**Use Cases:** The app returns the specific terms for that slot (Tariff, Grace Period, Cancellation Rules).
<details>
<summary><a href="../Example-schemas/04_on_select/ev-charging-select.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_select",
    "domain": "beckn.one:deg:ev-charging",
    "timestamp": "2024-01-15T10:30:05Z",
    "message_id": "bb9f86db-9a3d-4e9c-8c11-81c8f1a7b901",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "ecopower-charging",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/draft/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5"
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:acceptedOffer": {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
            "@type": "beckn:Offer",
            "beckn:id": "offer-ccs2-60kw-kwh",
            "beckn:descriptor": {
              "@type": "beckn:Descriptor",
              "schema:name": "Per-kWh Tariff - CCS2 60kW"
            },
            "beckn:items": [
              "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
            ],
            "beckn:provider": "ecopower-charging",
            "beckn:price": {
              "currency": "INR",
              "value": 45.0,
              "applicableQuantity": {
                "unitText": "Kilowatt Hour",
                "unitCode": "KWH",
                "unitQuantity": 1
              }
            }
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:orderAttributes": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
        "@type": "ChargingSession",
        "buyerFinderFee": {
          "feeType": "PERCENTAGE",
          "feeValue": 2.5
        },
        "preferences": {
          "startTime": "2026-01-04T08:00:00Z",
          "endTime": "2026-01-04T20:00:00Z"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.5. action: init**
**Method:** POST
**Use Cases:** Aisha provides her billing information (Credit Card details) for the ₹500 payment.
<details>
<summary><a href="../Example-schemas/05_init/ev-charging-init-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "init",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6743e9e2-4fb5-487c-92b7-13ba8018f176",
    "timestamp": "2025-01-27T10:00:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "INITIATED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012",
          "settlementAccounts": [
            {
              "beneficiaryId": "example-bap.com",
              "accountHolderName": "Example BAP Solutions Pvt Ltd",
              "accountNumber": "9876543210123",
              "ifscCode": "HDFC0009876",
              "bankName": "HDFC Bank",
              "vpa": "example-bap@paytm"
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.6. action: on_init**
**Method:** POST
**Use Cases:** The app presents the final payment terms and awaits authorization.
<details>
<summary><a href="../Example-schemas/06_on_init/ev-charging-on_init-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_init",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6743e9e2-4fb5-487c-92b7-13ba8018f176",
    "timestamp": "2025-01-27T10:00:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CREATED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:beneficiary": "BPP",
        "beckn:acceptedPaymentMethod": [
          "BANK_TRANSFER",
          "UPI",
          "WALLET"
        ],
        "beckn:paymentStatus": "INITIATED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012",
          "settlementAccounts": [
            {
              "beneficiaryId": "example-bap.com",
              "accountHolderName": "Example BAP Solutions Pvt Ltd",
              "accountNumber": "9876543210123",
              "ifscCode": "HDFC0009876",
              "bankName": "HDFC Bank",
              "vpa": "example-bap@paytm"
            },
            {
              "beneficiaryId": "example-bpp.com",
              "accountHolderName": "EcoPower Charging Solutions Pvt Ltd",
              "accountNumber": "1234567890123",
              "ifscCode": "HDFC0001234",
              "bankName": "HDFC Bank",
              "vpa": "ecopower@paytm"
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.6.1. action: on_status**
**Method:** POST
**Use Cases:** Application receives a notification on the completed status of the payment for the reservation.
<details>
<summary><a href="../Example-schemas/06_on_status_1/ev-charging-on_status-bpp.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "d4da89d5-2e42-4c36-9139-7f5682d5f104",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "PENDING",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.7. action: confirm**
**Method:** POST
**Use Cases:** Aisha confirms the reservation order.
<details>
<summary><a href="../Example-schemas/07_confirm/ev-charging-confirm.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "confirm",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "PENDING",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.8. action: on_confirm**
**Method:** POST
**Use Cases:** The application returns a unique Reservation ID confirming the slot is booked.
<details>
<summary><a href="../Example-schemas/08_00_on_confirm/ev-charging-on_confirm.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_confirm",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A",
          "beckn:quantity": {
            "unitText": "Kilowatt Hour",
            "unitCode": "KWH",
            "unitQuantity": 2.5
          },
          "beckn:price": {
            "currency": "INR",
            "value": 45.0,
            "applicableQuantity": {
              "unitText": "Kilowatt Hour",
              "unitCode": "KWH",
              "unitQuantity": 1
            }
          }
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.9. action: status**
**Method:** POST
**Use Cases:** Upon arrival, Aisha confirms she is at the right charger, the application checks the status of the reserved charger.
<details>
<summary><a href="../Example-schemas/08_01_status/ev-charging-connector-status.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.10. action: on_status**
**Method:** POST
**Use Cases:** The application confirms the charger is ready and prompts Aisha to "Start Charging" in the app.
<details>
<summary><a href="../Example-schemas/08_02_on_status/ev-charging-connector-on_status.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "c69b4c1e-fb7e-469d-ae90-00f4d5e82b64",
    "timestamp": "2025-01-27T10:05:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING",
          "connectorStatus": "PREPARING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.11. action: update (start charging)**
**Method:** POST
**Use Cases:** Aisha taps "Start Charging" and the app instructs the backend to energize the gun.
<details>
<summary><a href="../Example-schemas/09_update/ev-charging-start-update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6bd7be5b-ac21-4a5c-a787-5ec6980317e6",
    "timestamp": "2025-01-27T10:15:00Z",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "CONFIRMED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "connectorType": "CCS2",
          "maxPowerKW": 50,
          "sessionStatus": "PENDING"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.12. action: on_update (start charging)**
**Method:** POST
**Use Cases:** Response confirming the session has started successfully.
<details>
<summary><a href="../Example-schemas/10_on_update/ev-charging-start-on_update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6bd7be5b-ac21-4a5c-a787-5ec6980317e6",
    "timestamp": "2025-01-27T10:15:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "ACTIVE",
          "connectorType": "CCS2",
          "maxPowerKW": 50
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.13. action: track (charging-session progress)**
**Method:** POST
**Use Cases:** Aisha requests live telemetry (Energy dispensed, running cost) while at lunch.
<details>
<summary><a href="../Example-schemas/11_track/ev-charging-track.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "track",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6ace310b-6440-4421-a2ed-b484c7548bd5",
    "timestamp": "2025-01-27T17:00:40.065Z",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ]
    }
  },
  "error": {}
}
```
</details>

**13.2.2.14. action: on_track**
**Method:** POST
**Use Cases:** The app receives real-time updates on the charging progress.
<details>
<summary><a href="../Example-schemas/12_on_track/ev-charging-on_track.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_track",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "6ace310b-6440-4421-a2ed-b484c7548bd5",
    "timestamp": "2025-01-27T17:00:40.065Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "INPROGRESS",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "trackingAction": {
          "@type": "beckn:TrackAction",
          "target": {
            "@type": "schema:EntryPoint",
            "url": "https://track.bluechargenet-aggregator.io/session/SESSION-9876543210"
          }
        },
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "ACTIVE",
          "chargingTelemetry": [
            {
              "eventTime": "2025-01-27T17:00:00Z",
              "metrics": [
                {
                  "name": "STATE_OF_CHARGE",
                  "value": 62.5,
                  "unitCode": "PERCENTAGE"
                },
                {
                  "name": "POWER",
                  "value": 18.4,
                  "unitCode": "KWH"
                },
                {
                  "name": "ENERGY",
                  "value": 10.2,
                  "unitCode": "KW"
                },
                {
                  "name": "VOLTAGE",
                  "value": 392,
                  "unitCode": "VLT"
                },
                {
                  "name": "CURRENT",
                  "value": 47.0,
                  "unitCode": "AMP"
                }
              ]
            },
            {
              "eventTime": "2025-01-27T17:05:00Z",
              "metrics": [
                {
                  "name": "STATE_OF_CHARGE",
                  "value": 65.0,
                  "unitCode": "PERCENTAGE"
                },
                {
                  "name": "POWER",
                  "value": 17.1,
                  "unitCode": "KWH"
                },
                {
                  "name": "ENERGY",
                  "value": 11.1,
                  "unitCode": "KW"
                },
                {
                  "name": "VOLTAGE",
                  "value": 388,
                  "unitCode": "VLT"
                },
                {
                  "name": "CURRENT",
                  "value": 44.2,
                  "unitCode": "AMP"
                }
              ]
            }
          ]
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.15. async action: on_update (stop-charging)**
**Method:** POST
**Use Case:** The session terminates. Aisha receives the digital invoice and updated wallet balance.
<details>
<summary><a href="../Example-schemas/14_02_on_update/ev-charging-completed-on_update.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_update",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "32f67afe-3d8c-4faa-bc2e-93b0791dcb02",
    "timestamp": "2025-01-27T11:45:00Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "beckn:id": "order-ev-charging-001",
      "beckn:orderStatus": "COMPLETED",
      "beckn:seller": "cpo1.com",
      "beckn:buyer": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Buyer",
        "beckn:id": "user-123",
        "beckn:role": "BUYER",
        "beckn:displayName": "Ravi Kumar",
        "beckn:telephone": "+91-9876543210",
        "beckn:email": "ravi.kumar@example.com",
        "beckn:taxID": "GSTIN29ABCDE1234F1Z5",
        "beckn:buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "BuyerUPI",
          "vpa": "ravikumar@upi"
        }
      },
      "beckn:orderItems": [
        {
          "beckn:orderedItem": "IND*ecopower-charging*cs-01*IN*ECO*BTM*01*CCS2*A*CCS2-A"
        }
      ],
      "beckn:orderValue": {
        "currency": "INR",
        "value": 143.95,
        "components": [
          {
            "type": "UNIT",
            "value": 112.5,
            "currency": "INR",
            "description": "Base charging session cost (45 INR/kWh \u00d7 2.5 kWh)"
          },
          {
            "type": "SURCHARGE",
            "value": 20.0,
            "currency": "INR",
            "description": "Surge price (20%)"
          },
          {
            "type": "DISCOUNT",
            "value": -15.0,
            "currency": "INR",
            "description": "Offer discount (15%)"
          },
          {
            "type": "FEE",
            "value": 10.0,
            "currency": "INR",
            "description": "Service fee"
          },
          {
            "type": "FEE",
            "value": 13.64,
            "currency": "INR",
            "description": "Overcharge estimation"
          },
          {
            "type": "FEE",
            "value": 2.81,
            "currency": "INR",
            "description": "Buyer finder fee (2.5%)"
          }
        ]
      },
      "beckn:fulfillment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Fulfillment",
        "beckn:id": "fulfillment-001",
        "beckn:mode": "RESERVATION",
        "beckn:deliveryAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/EvChargingSession/v1/context.jsonld",
          "@type": "ChargingSession",
          "sessionStatus": "COMPLETED"
        }
      },
      "beckn:payment": {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:Payment",
        "beckn:id": "payment-123e4567-e89b-12d3-a456-426614174000",
        "beckn:amount": {
          "currency": "INR",
          "value": 143.95
        },
        "beckn:paymentURL": "https://payments.bluechargenet-aggregator.io/pay?transaction_id=$transaction_id&amount=$amount",
        "beckn:txnRef": "TXN-123456789",
        "beckn:paidAt": "2025-12-19T10:05:00Z",
        "beckn:beneficiary": "BPP",
        "beckn:paymentStatus": "COMPLETED",
        "beckn:paymentAttributes": {
          "@context": "https://raw.githubusercontent.com/bhim/ubc-tsd/main/beckn-schemas/UBCExtensions/v1/context.jsonld",
          "@type": "UBCPaymentAttributes",
          "upiTransactionId": "UPI123456789012"
        }
      }
    }
  },
  "error": {}
}
```
</details>

**13.2.2.16. action: rating**
**Method:** POST
**Use Cases:** Aisha provides a rating for the amenities and experience.
<details>
<summary><a href="../Example-schemas/15_rating/ev-charging-rating.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "rating",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "89ee20fe-b592-48b0-a5c5-e38f6b90e569",
    "timestamp": "2025-01-27T12:00:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "ratings": [
      {
        "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
        "@type": "beckn:RatingInput",
        "id": "fulfillment-001",
        "ratingValue": 4,
        "bestRating": 5,
        "worstRating": 1,
        "category": "FULFILLMENT",
        "feedback": {
          "comments": "Excellent charging experience! The station was clean, easy to find, and the charging was fast and reliable. The staff was helpful and the payment process was smooth.",
          "tags": [
            "fast-charging",
            "easy-to-use",
            "clean-station",
            "helpful-staff",
            "smooth-payment"
          ]
        }
      }
    ]
  },
  "error": {}
}
```
</details>

**13.2.2.17. action: on_rating**
**Method:** POST
**Use Cases:** Aisha receives an acknowledgement for her feedback.
<details>
<summary><a href="../Example-schemas/16_on_rating/ev-charging-on_rating.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_rating",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "89ee20fe-b592-48b0-a5c5-e38f6b90e569",
    "timestamp": "2025-01-27T12:00:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "received": true,
    "feedbackForm": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:Form",
      "url": "https://example-bpp.com/feedback/portal",
      "mime_type": "application/xml",
      "submission_id": "feedback-123e4567-e89b-12d3-a456-426614174000"
    }
  },
  "error": {}
}
```
</details>

**13.2.2.18. action: support**
**Method:** POST
**Use Cases:** Aisha reaches out for support if needed.
<details>
<summary><a href="../Example-schemas/17_support/ev-charging-support.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "support",
    "domain": "beckn.one:deg:ev-charging",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "dee432d9-36c9-4146-ad21-2f5bcac9b6a9",
    "timestamp": "2025-01-27T12:15:00Z",
    "ttl": "PT30S",
    "bap_id": "example-bap.com",
    "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2"
  },
  "message": {
    "refId": "order-ev-charging-001",
    "refType": "ORDER",
    "support": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:SupportInfo",
      "name": "Ravi Kumar",
      "phone": "+91-9876543210",
      "email": "ravi.kumar@example.com",
      "hours": "Mon\u2013Sun: 6:00 PM - 10:00 PM IST",
      "channels": [
        "PHONE",
        "WHATSAPP"
      ]
    }
  },
  "error": {}
}
```
</details>

**13.2.2.19. action: on_support**
**Method:** POST
**Use Cases:** Aisha receives a response to her support request.
<details>
<summary><a href="../Example-schemas/18_on_support/ev-charging-on_support.json">Example json :rocket:</a></summary>

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_support",
    "domain": "beckn.one:deg:ev-charging",
    "bap_id": "example-bap.com",
    "bap_uri": "https://example-bap.com/pilot/bap/energy/v2",
    "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
    "message_id": "dee432d9-36c9-4146-ad21-2f5bcac9b6a9",
    "timestamp": "2025-01-27T12:15:30Z",
    "ttl": "PT30S",
    "bpp_id": "example-bpp.com",
    "bpp_uri": "https://example-bpp.com/pilot/bpp/energy/v2"
  },
  "message": {
    "support": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/core-v2.0.0-rc/schema/core/v2/context.jsonld",
      "@type": "beckn:SupportInfo",
      "name": "BlueCharge Support Team",
      "phone": "18001080",
      "email": "support@bluechargenet-aggregator.io",
      "url": "https://support.bluechargenet-aggregator.io/ticket/SUP-20250730-001",
      "hours": "Mon\u2013Sun 24/7 IST",
      "channels": [
        "PHONE",
        "EMAIL",
        "WEB",
        "CHAT"
      ]
    }
  },
  "error": {}
}
```
</details>


## 13.3. FAQs


## 13.4. References

* [Postman collection for UEI EV Charging](https://github.com/beckn/missions/blob/main/UEI/postman/ev-charging_uei_postman_collection.json)  
* [Layer2 config for UEI EV Charging](https://github.com/beckn/missions/blob/main/UEI/layer2/EV-charging/3.1/energy_EV_1.1.0_openapi_3.1.yaml)  
* When installing layer2 using Beckn-ONIX use this web address ([https://raw.githubusercontent.com/beckn/missions/refs/heads/main/UEI/layer2/EV-charging/3.1/energy\_EV\_1.1.0\_openapi\_3.1.yaml](https://raw.githubusercontent.com/beckn/missions/refs/heads/main/UEI/layer2/EV-charging/3.1/energy_EV_1.1.0_openapi_3.1.yaml))


