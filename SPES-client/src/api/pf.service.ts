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
/* tslint:disable:no-unused-variable member-ordering */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,
         HttpResponse, HttpEvent, HttpParameterCodec, HttpContext
        }       from '@angular/common/http';
import { CustomHttpParameterCodec }                          from '../encoder';
import { Observable }                                        from 'rxjs';

// @ts-ignore
import { Address } from '../model/address';
// @ts-ignore
import { Citizenship } from '../model/citizenship';
// @ts-ignore
import { HTTPValidationError } from '../model/hTTPValidationError';
// @ts-ignore
import { MaritalStatus } from '../model/maritalStatus';
// @ts-ignore
import { PFPartialInfoWithIds } from '../model/pFPartialInfoWithIds';
// @ts-ignore
import { PfId } from '../model/pfId';
// @ts-ignore
import { PfInfo } from '../model/pfInfo';
// @ts-ignore
import { PfInfoWithIds } from '../model/pfInfoWithIds';
// @ts-ignore
import { PfInfoWithIdsForUpdate } from '../model/pfInfoWithIdsForUpdate';
// @ts-ignore
import { UserInfoForUpdate } from '../model/userInfoForUpdate';
// @ts-ignore
import { UserInfoWithPwd } from '../model/userInfoWithPwd';

// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';



@Injectable({
  providedIn: 'root'
})
export class PfService {

    protected basePath = 'http://localhost:8080';
    public defaultHeaders = new HttpHeaders();
    public configuration = new Configuration();
    public encoder: HttpParameterCodec;

    constructor(protected httpClient: HttpClient, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {
        if (configuration) {
            this.configuration = configuration;
        }
        if (typeof this.configuration.basePath !== 'string') {
            if (typeof basePath !== 'string') {
                basePath = this.basePath;
            }
            this.configuration.basePath = basePath;
        }
        this.encoder = this.configuration.encoder || new CustomHttpParameterCodec();
    }


    private addToHttpParams(httpParams: HttpParams, value: any, key?: string): HttpParams {
        if (typeof value === "object" && value instanceof Date === false) {
            httpParams = this.addToHttpParamsRecursive(httpParams, value);
        } else {
            httpParams = this.addToHttpParamsRecursive(httpParams, value, key);
        }
        return httpParams;
    }

    private addToHttpParamsRecursive(httpParams: HttpParams, value?: any, key?: string): HttpParams {
        if (value == null) {
            return httpParams;
        }

        if (typeof value === "object") {
            if (Array.isArray(value)) {
                (value as any[]).forEach( elem => httpParams = this.addToHttpParamsRecursive(httpParams, elem, key));
            } else if (value instanceof Date) {
                if (key != null) {
                    httpParams = httpParams.append(key,
                        (value as Date).toISOString().substr(0, 10));
                } else {
                   throw Error("key may not be null if value is Date");
                }
            } else {
                Object.keys(value).forEach( k => httpParams = this.addToHttpParamsRecursive(
                    httpParams, value[k], key != null ? `${key}.${k}` : k));
            }
        } else if (key != null) {
            httpParams = httpParams.append(key, value);
        } else {
            throw Error("key may not be null if value is not object or array");
        }
        return httpParams;
    }

    /**
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID.
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID. Tale operazione può essere effettuata solamente dagli OPS.
     * @param idPf ID univoco della persona fragile
     * @param address
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public addAddressByPfIdPfIdPfAddressPost(idPf: string, address?: Array<Address>, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any>;
    public addAddressByPfIdPfIdPfAddressPost(idPf: string, address?: Array<Address>, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<any>>;
    public addAddressByPfIdPfIdPfAddressPost(idPf: string, address?: Array<Address>, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<any>>;
    public addAddressByPfIdPfIdPfAddressPost(idPf: string, address?: Array<Address>, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling addAddressByPfIdPfIdPfAddressPost.');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.post<any>(`${this.configuration.basePath}/pf/${encodeURIComponent(String(idPf))}/address`,
            address,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID.
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID. Tale operazione può essere effettuata solamente dagli OPS.
     * @param idPf ID univoco della persona fragile
     * @param citizenship
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public addCitizenshipByPfIdPfIdPfCitizenshipPost(idPf: string, citizenship?: Array<Citizenship>, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any>;
    public addCitizenshipByPfIdPfIdPfCitizenshipPost(idPf: string, citizenship?: Array<Citizenship>, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<any>>;
    public addCitizenshipByPfIdPfIdPfCitizenshipPost(idPf: string, citizenship?: Array<Citizenship>, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<any>>;
    public addCitizenshipByPfIdPfIdPfCitizenshipPost(idPf: string, citizenship?: Array<Citizenship>, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling addCitizenshipByPfIdPfIdPfCitizenshipPost.');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.post<any>(`${this.configuration.basePath}/pf/${encodeURIComponent(String(idPf))}/citizenship`,
            citizenship,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID.
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID. Tale operazione può essere effettuata solamente dagli OPS.
     * @param idPf ID univoco della persona fragile
     * @param maritalStatus
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public addMaritalStatusByPfIdPfIdPfMaritalStatusPost(idPf: string, maritalStatus?: Array<MaritalStatus>, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any>;
    public addMaritalStatusByPfIdPfIdPfMaritalStatusPost(idPf: string, maritalStatus?: Array<MaritalStatus>, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<any>>;
    public addMaritalStatusByPfIdPfIdPfMaritalStatusPost(idPf: string, maritalStatus?: Array<MaritalStatus>, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<any>>;
    public addMaritalStatusByPfIdPfIdPfMaritalStatusPost(idPf: string, maritalStatus?: Array<MaritalStatus>, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling addMaritalStatusByPfIdPfIdPfMaritalStatusPost.');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.post<any>(`${this.configuration.basePath}/pf/${encodeURIComponent(String(idPf))}/marital_status`,
            maritalStatus,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Ottiene i dati anagrafici di una PF a partire dal suo id.
     * Ottiene i dati anagrafici di una PF a partire dal suo id.
     * @param idPf ID univoco della persona fragile
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getPfInfoByIdPfIdPfGet(idPf: string, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<PfInfoWithIds>;
    public getPfInfoByIdPfIdPfGet(idPf: string, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<PfInfoWithIds>>;
    public getPfInfoByIdPfIdPfGet(idPf: string, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<PfInfoWithIds>>;
    public getPfInfoByIdPfIdPfGet(idPf: string, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling getPfInfoByIdPfIdPfGet.');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.get<PfInfoWithIds>(`${this.configuration.basePath}/pf/${encodeURIComponent(String(idPf))}`,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Registra una PF nel sistema.
     * - Effettua la registrazione di una PFnel sistema, inserendo i suoi dati anagrafici. Tale registrazione può essere effettuata solamente dagli OPS.
     * @param pfInfo
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public registerPfPfPost(pfInfo?: PfInfo, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any>;
    public registerPfPfPost(pfInfo?: PfInfo, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<any>>;
    public registerPfPfPost(pfInfo?: PfInfo, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<any>>;
    public registerPfPfPost(pfInfo?: PfInfo, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.post<any>(`${this.configuration.basePath}/pf`,
            pfInfo,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Restituisce una lista di PF in base alla query sottomessa.
     * Effettua una ricerca della PF sottoponendo al sistema una query. Tale ricerca può essere effettuata da OPS e MED.
     * @param firstname Il nome della persona fragile.
     * @param lastname Il cognome della persona fragile.
     * @param nicknames Il nickname della persona fragile.
     * @param cf Il codice fiscale della persona fragile.
     * @param isAnonymous La persona fragile è anonima?
     * @param isForeign La persona fragile è straniera?
     * @param isDead La persona fragile è morta?
     * @param verified La persona fragile è stata verificata?
     * @param offset Offset della ricerca.
     * @param limit Limit della ricerca.
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public searchPfsByQuerySearchPfGet(firstname?: string, lastname?: string, nicknames?: string, cf?: string, isAnonymous?: boolean, isForeign?: boolean, isDead?: boolean, verified?: boolean, offset?: number, limit?: number, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<Array<PFPartialInfoWithIds>>;
    public searchPfsByQuerySearchPfGet(firstname?: string, lastname?: string, nicknames?: string, cf?: string, isAnonymous?: boolean, isForeign?: boolean, isDead?: boolean, verified?: boolean, offset?: number, limit?: number, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<Array<PFPartialInfoWithIds>>>;
    public searchPfsByQuerySearchPfGet(firstname?: string, lastname?: string, nicknames?: string, cf?: string, isAnonymous?: boolean, isForeign?: boolean, isDead?: boolean, verified?: boolean, offset?: number, limit?: number, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<Array<PFPartialInfoWithIds>>>;
    public searchPfsByQuerySearchPfGet(firstname?: string, lastname?: string, nicknames?: string, cf?: string, isAnonymous?: boolean, isForeign?: boolean, isDead?: boolean, verified?: boolean, offset?: number, limit?: number, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {

        let localVarQueryParameters = new HttpParams({encoder: this.encoder});
        if (firstname !== undefined && firstname !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>firstname, 'firstname');
        }
        if (lastname !== undefined && lastname !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>lastname, 'lastname');
        }
        if (nicknames !== undefined && nicknames !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>nicknames, 'nicknames');
        }
        if (cf !== undefined && cf !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>cf, 'cf');
        }
        if (isAnonymous !== undefined && isAnonymous !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>isAnonymous, 'is_anonymous');
        }
        if (isForeign !== undefined && isForeign !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>isForeign, 'is_foreign');
        }
        if (isDead !== undefined && isDead !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>isDead, 'is_dead');
        }
        if (verified !== undefined && verified !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>verified, 'verified');
        }
        if (offset !== undefined && offset !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>offset, 'offset');
        }
        if (limit !== undefined && limit !== null) {
          localVarQueryParameters = this.addToHttpParams(localVarQueryParameters,
            <any>limit, 'limit');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.get<Array<PFPartialInfoWithIds>>(`${this.configuration.basePath}/search/pf`,
            {
                context: localVarHttpContext,
                params: localVarQueryParameters,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID.
     * Aggiorna i dati anagrafici di una PF a partire dal suo ID. Tale operazione può essere effettuata solamente dagli OPS.
     * @param idPf ID univoco della persona fragile
     * @param pfInfoWithIdsForUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public updatePfInfoByIdPfIdPfPatch(idPf: string, pfInfoWithIdsForUpdate?: PfInfoWithIdsForUpdate, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any>;
    public updatePfInfoByIdPfIdPfPatch(idPf: string, pfInfoWithIdsForUpdate?: PfInfoWithIdsForUpdate, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<any>>;
    public updatePfInfoByIdPfIdPfPatch(idPf: string, pfInfoWithIdsForUpdate?: PfInfoWithIdsForUpdate, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<any>>;
    public updatePfInfoByIdPfIdPfPatch(idPf: string, pfInfoWithIdsForUpdate?: PfInfoWithIdsForUpdate, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling updatePfInfoByIdPfIdPfPatch.');
        }

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.patch<any>(`${this.configuration.basePath}/pf/${encodeURIComponent(String(idPf))}`,
            pfInfoWithIdsForUpdate,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Aggiorna lo user a partire dal pf_id
     * Aggiorna lo user a partire dal pf_id
     * @param userInfoForUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public updatePfUserInfoUserPfPatch(userInfoForUpdate?: UserInfoForUpdate, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<UserInfoWithPwd>;
    public updatePfUserInfoUserPfPatch(userInfoForUpdate?: UserInfoForUpdate, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<UserInfoWithPwd>>;
    public updatePfUserInfoUserPfPatch(userInfoForUpdate?: UserInfoForUpdate, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<UserInfoWithPwd>>;
    public updatePfUserInfoUserPfPatch(userInfoForUpdate?: UserInfoForUpdate, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {

        let localVarHeaders = this.defaultHeaders;

        let localVarCredential: string | undefined;
        // authentication (HTTPBearer) required
        localVarCredential = this.configuration.lookupCredential('HTTPBearer');
        if (localVarCredential) {
            localVarHeaders = localVarHeaders.set('Authorization', 'Bearer ' + localVarCredential);
        }

        let localVarHttpHeaderAcceptSelected: string | undefined = options && options.httpHeaderAccept;
        if (localVarHttpHeaderAcceptSelected === undefined) {
            // to determine the Accept header
            const httpHeaderAccepts: string[] = [
                'application/json'
            ];
            localVarHttpHeaderAcceptSelected = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        }
        if (localVarHttpHeaderAcceptSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Accept', localVarHttpHeaderAcceptSelected);
        }

        let localVarHttpContext: HttpContext | undefined = options && options.context;
        if (localVarHttpContext === undefined) {
            localVarHttpContext = new HttpContext();
        }


        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            localVarHeaders = localVarHeaders.set('Content-Type', httpContentTypeSelected);
        }

        let responseType_: 'text' | 'json' | 'blob' = 'json';
        if (localVarHttpHeaderAcceptSelected) {
            if (localVarHttpHeaderAcceptSelected.startsWith('text')) {
                responseType_ = 'text';
            } else if (this.configuration.isJsonMime(localVarHttpHeaderAcceptSelected)) {
                responseType_ = 'json';
            } else {
                responseType_ = 'blob';
            }
        }

        return this.httpClient.patch<UserInfoWithPwd>(`${this.configuration.basePath}/user/pf`,
            userInfoForUpdate,
            {
                context: localVarHttpContext,
                responseType: <any>responseType_,
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

}