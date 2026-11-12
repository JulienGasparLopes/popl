"use client"

const SERVER_URL = `${window.location.protocol}//${window.location.host}`

export const Sidebar = ({ session }) => {
    return (<nav className="p-8 shadow-xl/30 min-w-60">
        <div className="grid grid-cols-1 grid-rows-[auto_auto_1fr_auto] justify-stretch h-full">

            <div className="flex content-center flex-col items-center mb-16 leading-none">
                <h1>Path</h1>
                <h1>of</h1>
                <h1>Private</h1>
                <h1>League</h1>
            </div>

            <hr className="mb-16"></hr>

            <div className="flex flex-col gap-4">
                <a href="/mechanics">
                    <h2>League Mechanics</h2>
                </a>

                <a href="/builds">
                    <h2>Builds</h2>
                </a>

                <a href="/wantedItems">
                    <h2>Wish List</h2>
                </a>
            </div>

            <div className="self-end">
                {

                    session ? (
                        <>
                            <div>Logged in as</div>
                            <div>{session.pseudo}</div>
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

            </div>
        </div>

    </nav>)
}
