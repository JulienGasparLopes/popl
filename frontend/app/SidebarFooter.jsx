"use client"

export const SidebarFooter = ({ session }) => {
    return (<div className="self-end">
        {
            session ? (
                <>
                    <div>Logged in as</div>
                    <div >{session.pseudo}</div>
                    <a href={"/api/logout"}>
                        Logout
                    </a>
                </>
            ) :
                (
                    <a href={"/api/auth/google/login"}>
                        Sign in with Google
                    </a>
                )
        }
    </div>)
}