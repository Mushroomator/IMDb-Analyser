/**
 * Checks whether an index is valid to access the array or not.
 * 
 * An index is valid if all of the following conditions are met
 *  - index is not undefined
 *  - index is an integer
 *  - index is greater or equal to zero
 *  - index is smaller than the length of the array
 *  
 * @param idx index to be checked
 * @param arrLen length of array in question
 * @returns true if index is valid, false otherwise
 */
export function isValidArrIdx(idx: number | undefined, arrLen: number): boolean{
    if(idx 
        && Number.isInteger(idx)
        && idx >= 0 
        && idx < arrLen) return true;
    return false;
}