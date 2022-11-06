from icmplib import async_multiping, NameLookupError
import socket


async def are_alive(addresses, count=1, interval=0.5, timeout=0.5):
    results = []
    try:
        hosts = await async_multiping(
            addresses,
            count=count,
            interval=interval,
            concurrent_tasks=50,
            privileged=True,
            timeout=timeout,
        )
    except NameLookupError as error:
        results.append({"error": str(error)})
        # print(error)
        # print(results)
        return results
    for host in hosts:
        hostname = [None]
        try:
            hostname = socket.gethostbyaddr(host.address)
        except Exception as error:
            print(error)
        results.append(
            {
                "is_alive": host.is_alive,
                "address": host.address,
                "hostname": hostname[0],
                "min_rtt": host.min_rtt,
                "max_rtt": host.max_rtt,
                "avg_rtt": host.avg_rtt,
                "packets_sent": host.packets_sent,
                "packets_received": host.packets_received,
                "packet_loss": host.packet_loss,
                "jitter": host.jitter,
                "rtts": host.rtts,
            }
        )

    return results
