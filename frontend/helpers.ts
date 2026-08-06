import { SubmitEvent } from "react";


export const formEventToData = (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    var object = {};
    formData.forEach((value, key) => object[key] = value);
    return object;
}