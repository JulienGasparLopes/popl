import { SubmitEvent } from "react";


type BuildSetInfo = { pob_code: string, build_set_id: string }

type formEventToDataType = (event: SubmitEvent<HTMLFormElement>) => BuildSetInfo

export const formEventToData: formEventToDataType = (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    var object = {};
    formData.forEach((value, key) => object[key] = value);
    return object;
}