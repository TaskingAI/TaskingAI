import { Suspense } from "react"

const lazyLoad=(Comp:React.ComponentType<object>)=>{
    return (
        <Suspense>
            <Comp></Comp>
        </Suspense>
    )
}
export default lazyLoad