/**
 * SPES
 * ### Documentazione Termini chiave:   - PF: persona fragile   - MED: medico   - OPS: Operatore Sociosanitario (o chi ne fa le veci)   Autori:   - Luca Gregori   - Alessandro Wood 
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { MaritalStatus } from './maritalStatus';
import { Address } from './address';
import { Citizenship } from './citizenship';


/**
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).  Do not edit the class manually.  PfInfo - a model defined in OpenAPI      cf: The cf of this PfInfo [Optional].     firstname: The firstname of this PfInfo.     lastname: The lastname of this PfInfo.     fullname: The fullname of this PfInfo [Optional].     gender: The gender of this PfInfo [Optional].     nicknames: The nicknames of this PfInfo [Optional].     birth_date: The birth_date of this PfInfo [Optional].     birth_nation_id: The birth_nation_id of this PfInfo [Optional].     birth_geoarea_id: The birth_geoarea_id of this PfInfo [Optional].     birth_city: The birth_city of this PfInfo [Optional].     cui_code: The cui_code of this PfInfo [Optional].     sanitary_district_id: The sanitary_district_id of this PfInfo [Optional].     is_foreign: The is_foreign of this PfInfo [Optional].     verified: The verified of this PfInfo [Optional].     is_dead: The is_dead of this PfInfo [Optional].     death_date: The death_date of this PfInfo [Optional].
 */
export interface PfInfoWithIds { 
    cf?: string;
    firstname: string;
    lastname: string;
    fullname?: string;
    gender?: string;
    nicknames?: string;
    birth_date?: string;
    birth_nation_id?: string;
    birth_geoarea_id?: number;
    birth_city?: string;
    cui_code?: string;
    sanitary_district_id?: number;
    is_foreign?: boolean;
    is_anonymous?: boolean;
    verified?: boolean;
    is_dead?: boolean;
    death_date?: string;
    marital_status_list?: { [key: string]: MaritalStatus; };
    address_list?: { [key: string]: Address; };
    citizenship_list?: { [key: string]: Citizenship; };
    pf_id: string;
}

