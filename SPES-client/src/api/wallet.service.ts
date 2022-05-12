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
import { DocPartialInfo } from '../model/docPartialInfo';
// @ts-ignore
import { HTTPValidationError } from '../model/hTTPValidationError';

// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';



@Injectable({
  providedIn: 'root'
})
export class WalletService {

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

    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    private canConsumeForm(consumes: string[]): boolean {
        const form = 'multipart/form-data';
        for (const consume of consumes) {
            if (form === consume) {
                return true;
            }
        }
        return false;
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
     * Restituisce il documento indetificativo della PF in base all&amp;#39;ID.
     * - Restituisce il documento indetificativo della PF in base all&amp;#39;ID.
     * @param idPf ID univoco della persona fragile
     * @param docId ID univoco del documento identificativo.
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf: string, docId: string, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json' | 'application/pdf', context?: HttpContext}): Observable<Blob>;
    public getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf: string, docId: string, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json' | 'application/pdf', context?: HttpContext}): Observable<HttpResponse<Blob>>;
    public getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf: string, docId: string, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json' | 'application/pdf', context?: HttpContext}): Observable<HttpEvent<Blob>>;
    public getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf: string, docId: string, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json' | 'application/pdf', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet.');
        }
        if (docId === null || docId === undefined) {
            throw new Error('Required parameter docId was null or undefined when calling getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet.');
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
                'application/json',
                'application/pdf'
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


        return this.httpClient.get(`${this.configuration.basePath}/wallet/pf/${encodeURIComponent(String(idPf))}/docs/${encodeURIComponent(String(docId))}`,
            {
                context: localVarHttpContext,
                responseType: "blob",
                withCredentials: this.configuration.withCredentials,
                headers: localVarHeaders,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Restituisce la lista dei documenti identificativi associati alla PF
     * - Restituisce la lista dei documenti identificativi associati alla PF.
     * @param idPf ID univoco della persona fragile
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getIdentificationDocumentsWalletPfIdPfDocsGet(idPf: string, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<Array<DocPartialInfo>>;
    public getIdentificationDocumentsWalletPfIdPfDocsGet(idPf: string, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<Array<DocPartialInfo>>>;
    public getIdentificationDocumentsWalletPfIdPfDocsGet(idPf: string, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<Array<DocPartialInfo>>>;
    public getIdentificationDocumentsWalletPfIdPfDocsGet(idPf: string, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling getIdentificationDocumentsWalletPfIdPfDocsGet.');
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

        return this.httpClient.get<Array<DocPartialInfo>>(`${this.configuration.basePath}/wallet/pf/${encodeURIComponent(String(idPf))}/docs`,
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
     * Aggiorna il documento identificativo della persona fragile.
     * - Effettua un aggiornamento del documento indentificativo della PF (chiamata soggetta a rimozione nel caso si volesse mantenere uno storico dei documenti identificativi per tipologia).
     * @param idPf ID univoco della persona fragile
     * @param docId ID univoco del documento identificativo.
     * @param doc
     * @param tipologia Tipologia di documento.
     * @param entity Ente di rilascio.
     * @param number Numero del documento.
     * @param placeOfIssue Luogo di rilascio.
     * @param releaseDate Data di rilascio.
     * @param expirationDate Data di scadenza.
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut(idPf: string, docId: string, doc?: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<DocPartialInfo>;
    public updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut(idPf: string, docId: string, doc?: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<DocPartialInfo>>;
    public updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut(idPf: string, docId: string, doc?: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<DocPartialInfo>>;
    public updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut(idPf: string, docId: string, doc?: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut.');
        }
        if (docId === null || docId === undefined) {
            throw new Error('Required parameter docId was null or undefined when calling updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut.');
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
            'multipart/form-data'
        ];

        const canConsumeForm = this.canConsumeForm(consumes);

        let localVarFormParams: { append(param: string, value: any): any; };
        let localVarUseForm = false;
        let localVarConvertFormParamsToString = false;
        // use FormData to transmit files using content-type "multipart/form-data"
        // see https://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
        localVarUseForm = canConsumeForm;
        if (localVarUseForm) {
            localVarFormParams = new FormData();
        } else {
            localVarFormParams = new HttpParams({encoder: this.encoder});
        }

        if (tipologia !== undefined) {
            localVarFormParams = localVarFormParams.append('tipologia', <any>tipologia) as any || localVarFormParams;
        }
        if (entity !== undefined) {
            localVarFormParams = localVarFormParams.append('entity', <any>entity) as any || localVarFormParams;
        }
        if (number !== undefined) {
            localVarFormParams = localVarFormParams.append('number', <any>number) as any || localVarFormParams;
        }
        if (placeOfIssue !== undefined) {
            localVarFormParams = localVarFormParams.append('place_of_issue', <any>placeOfIssue) as any || localVarFormParams;
        }
        if (releaseDate !== undefined) {
            localVarFormParams = localVarFormParams.append('release_date', <any>releaseDate) as any || localVarFormParams;
        }
        if (expirationDate !== undefined) {
            localVarFormParams = localVarFormParams.append('expiration_date', <any>expirationDate) as any || localVarFormParams;
        }
        if (doc !== undefined) {
            localVarFormParams = localVarFormParams.append('doc', <any>doc) as any || localVarFormParams;
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

        return this.httpClient.put<DocPartialInfo>(`${this.configuration.basePath}/wallet/pf/${encodeURIComponent(String(idPf))}/docs/${encodeURIComponent(String(docId))}`,
            localVarConvertFormParamsToString ? localVarFormParams.toString() : localVarFormParams,
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
     * Upload dei documenti identificativi di una PF.
     * - Effettua l\&#39;upload di un documento identificativo della persona fragile. Tale operazione può essere effettuata solamente dagli OPS.
     * @param idPf ID univoco della persona fragile
     * @param doc
     * @param tipologia Tipologia di documento.
     * @param entity Ente di rilascio.
     * @param number Numero del documento.
     * @param placeOfIssue Luogo di rilascio.
     * @param releaseDate Data di rilascio.
     * @param expirationDate Data di scadenza.
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public uploadIdentificationDocumentWalletPfIdPfDocsUploadPost(idPf: string, doc: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'body', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<DocPartialInfo>;
    public uploadIdentificationDocumentWalletPfIdPfDocsUploadPost(idPf: string, doc: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'response', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpResponse<DocPartialInfo>>;
    public uploadIdentificationDocumentWalletPfIdPfDocsUploadPost(idPf: string, doc: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe?: 'events', reportProgress?: boolean, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<HttpEvent<DocPartialInfo>>;
    public uploadIdentificationDocumentWalletPfIdPfDocsUploadPost(idPf: string, doc: Blob, tipologia?: string, entity?: string, number?: string, placeOfIssue?: string, releaseDate?: string, expirationDate?: string, observe: any = 'body', reportProgress: boolean = false, options?: {httpHeaderAccept?: 'application/json', context?: HttpContext}): Observable<any> {
        if (idPf === null || idPf === undefined) {
            throw new Error('Required parameter idPf was null or undefined when calling uploadIdentificationDocumentWalletPfIdPfDocsUploadPost.');
        }
        if (doc === null || doc === undefined) {
            throw new Error('Required parameter doc was null or undefined when calling uploadIdentificationDocumentWalletPfIdPfDocsUploadPost.');
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
            'multipart/form-data'
        ];

        const canConsumeForm = this.canConsumeForm(consumes);

        let localVarFormParams: { append(param: string, value: any): any; };
        let localVarUseForm = false;
        let localVarConvertFormParamsToString = false;
        // use FormData to transmit files using content-type "multipart/form-data"
        // see https://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
        localVarUseForm = canConsumeForm;
        if (localVarUseForm) {
            localVarFormParams = new FormData();
        } else {
            localVarFormParams = new HttpParams({encoder: this.encoder});
        }

        if (tipologia !== undefined) {
            localVarFormParams = localVarFormParams.append('tipologia', <any>tipologia) as any || localVarFormParams;
        }
        if (entity !== undefined) {
            localVarFormParams = localVarFormParams.append('entity', <any>entity) as any || localVarFormParams;
        }
        if (number !== undefined) {
            localVarFormParams = localVarFormParams.append('number', <any>number) as any || localVarFormParams;
        }
        if (placeOfIssue !== undefined) {
            localVarFormParams = localVarFormParams.append('place_of_issue', <any>placeOfIssue) as any || localVarFormParams;
        }
        if (releaseDate !== undefined) {
            localVarFormParams = localVarFormParams.append('release_date', <any>releaseDate) as any || localVarFormParams;
        }
        if (expirationDate !== undefined) {
            localVarFormParams = localVarFormParams.append('expiration_date', <any>expirationDate) as any || localVarFormParams;
        }
        if (doc !== undefined) {
            localVarFormParams = localVarFormParams.append('doc', <any>doc) as any || localVarFormParams;
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

        return this.httpClient.post<DocPartialInfo>(`${this.configuration.basePath}/wallet/pf/${encodeURIComponent(String(idPf))}/docs/upload`,
            localVarConvertFormParamsToString ? localVarFormParams.toString() : localVarFormParams,
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
