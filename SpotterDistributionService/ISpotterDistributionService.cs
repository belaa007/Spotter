using System;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Threading.Tasks;
using SpotterDataTransferObject;

namespace SpotterDistributionService
{
    /// <summary>
    /// SpotterDistributionService interface
    /// </summary>
    [ServiceContract]
    public interface ISpotterDistributionService
    {
        /// <summary>
        /// Pings the specified parameter.
        /// </summary>
        /// <param name="parameter">The parameter.</param>
        /// <returns></returns>
        [OperationContract]
        PingResult Ping(PingParameter parameter);

        /// <summary>
        /// FPings the specified parameter.
        /// </summary>
        /// <param name="parameter">The parameter.</param>
        /// <returns></returns>
        [OperationContract]
        FPingResult FPing(FPingParameter parameter);

        /// <summary>
        /// Updates the specified node.
        /// </summary>
        /// <param name="nodeName">Name of the node.</param>
        /// <param name="nodeAddress">The node address.</param>
        /// <returns></returns>
        [OperationContract]
        [WebInvoke(Method = "POST",
            UriTemplate = "Update/{nodeName}/{nodeAddress}")]
        String Update(String nodeName, String nodeAddress);
    }

}
