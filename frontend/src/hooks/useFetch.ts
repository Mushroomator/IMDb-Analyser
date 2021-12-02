import { useCallback, useEffect, useRef, useState } from "react";

export function useFetch<DataType, ResponseType>(
    input: RequestInfo,
    initialState: DataType,
    transformReq2Data: (resObj: ResponseType) => DataType,
    init?: RequestInit | undefined) {

    const [data, setData] = useState<DataType>(initialState);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<null | Error>(null);
    const [run, setRun] = useState<boolean>(true);
    const timeoutInMs = useRef<number>(1000);
    const maxTimeout = useRef<number>(30000);

    /**
    * Memoize the fetch function so it is only created once when props change, 
    * not on every re-render due to state changes
    */
    const fetchData = useCallback(() => {
        if(run){
            console.log("Updating useCallback function")
            fetch(input, init)
                .then(async res => {
                    const parsed: ResponseType = await res.json().catch(err => console.log(err));
                    setData(transformReq2Data(parsed));
                    setIsLoading(false);
                })
                .catch(err => {
                    let newTimeout = timeoutInMs.current * 2;
                    if(newTimeout > maxTimeout.current) newTimeout = maxTimeout.current;
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
        console.log("Running use effect fetch data")
        fetchData()
    }, [fetchData]);


    return { isLoading, error, data }
}