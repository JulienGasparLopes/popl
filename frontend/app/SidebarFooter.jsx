"use client"

export const SidebarFooter = ({ session }) => {
    return (<div className="self-end">
        {
            session ? (
                <>
                    <div>Logged in as</div>
                    <div >{session.pseudo}</div>
                    <a href={"/api/auth/logout"}>
                        Logout
                    </a>
                </>
            ) :
                (
                    <a href={"/api/auth/login"}>
                        Sign in with Google
                    </a>
                )
        }
    </div>)
}