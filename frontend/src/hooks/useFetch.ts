import { useCallback, useEffect, useRef, useState } from "react";
import { IError } from "../types";

export function useFetch<DataType, ResponseType>(
    input: RequestInfo,
    initialState: DataType,
    transformReq2Data: (resObj: ResponseType) => DataType,
    init?: RequestInit | undefined) {

    const [data, setData] = useState<DataType>(initialState);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<null | IError>(null);
    const [run, setRun] = useState<boolean>(true);
    const timeoutInMs = useRef<number>(1000);
    const maxTimeout = useRef<number>(30000);

    /**
    * Memoize the fetch function so it is only created once when props change, 
    * not on every re-render due to state changes
    */
    const fetchData = useCallback(() => {
        if (run) {
            fetch(input, init)
                .then(async res => {
                    if(res.status !== 200){
                        setError({
                            title: "No successful connection",
                            desc: `Failed to fetch data from backend! Status code: ${res.status}`
                        })
                    } else {
                        try {
                            const parsed: ResponseType = await res.json()
                            setData(transformReq2Data(parsed));
                            setIsLoading(false);
                        }
                        catch (err) {
                            console.log(err)
                        }
                    }
                })
                .catch(err => {
                    let newTimeout = timeoutInMs.current * 2;
                    if (newTimeout > maxTimeout.current) newTimeout = maxTimeout.current;
                    timeoutInMs.current = newTimeout;
                    setError(err)
                    setTimeout(() => setRun(true), timeoutInMs.current)
                });
            setRun(false)
        }
    }, [run])

    /**
     * Get all actors from the api
     */
    useEffect(() => {
        fetchData()
    }, [fetchData]);


    return { isLoading, error, data }
}