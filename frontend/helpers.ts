import { SubmitEvent } from "react";


type BuildSetInfo = { pob_code: string, build_set_id: string | null }

type formEventToDataType = (event: SubmitEvent<HTMLFormElement>) => BuildSetInfo

export const formEventToData: formEventToDataType = (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    var object: BuildSetInfo = {
        pob_code: formData.get("pob_code")!.toString(),
        build_set_id: formData.get("build_set_id")?.toString() || null
    }
    return object;
}