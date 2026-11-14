"use client"



export const SidebarFooter = ({ session }) => {
    const SERVER_URL = `${window.location.protocol}//${window.location.hostname}:5000`

    return (<div className="self-end">
        {

            session ? (
                <>
                    <div>Logged in as</div>
                    <div >{session.pseudo}</div>
                    <a href={`${SERVER_URL}/logout`}>
                        Logout
                    </a>
                </>

            ) :
                (
                    <a href={`${SERVER_URL}/auth/google/login`}>
                        Sign in with Google
                    </a>
                )
        }
    </div>)
}