using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Runtime.Serialization.Json;
using System.Threading.Tasks;
using System.Web.UI;
using System.Web.UI.WebControls;
using SpotterDataTransferObject;
using SpotterDataTransferObject.PythonComm;

namespace SpotterDistributionService
{
    /// <summary>
    /// Class implementing the SpotterDistribtuionService interface
    /// </summary>
    public class SpotterDistributionService : ISpotterDistributionService
    {
        /// <summary>
        /// The _entities
        /// </summary>
        private readonly SpotterDatabaseEntities _entities;

        /// <summary>
        /// Initializes a new instance of the <see cref="SpotterDistributionService"/> class.
        /// </summary>
        public SpotterDistributionService() { _entities = new SpotterDatabaseEntities(); }

        /// <summary>
        /// Pings the specified parameter.
        /// </summary>
        /// <param name="parameter">The parameter.</param>
        /// <returns></returns>
        public PingResult Ping(PingParameter parameter)
        {
            return PingTask(parameter).Result;
        }

        /// <summary>
        /// Exectutes the ping request on the selected nodes asynchronously
        /// </summary>
        /// <param name="parameter">The parameter.</param>
        /// <returns></returns>
        private async Task<PingResult> PingTask(PingParameter parameter)
        {
            var result = new PingResult { Nodes = new List<Node>(), Replies = new List<PingReply>() };
            //TODO Betenni egy szűrést, hogy csak a <15 perce bejelentkezett nodeokat, és régiónként csak egyet.
            var nodes = _entities.Nodes.ToList();
            var taskList = new List<Task<PingReply>>();

            foreach (var node in nodes)
            {
                var tnode = new Node()
                {
                    Id = node.Id,
                    Address = node.Address,
                    LastCheckin = node.LastCheckin,
                    Latitude = node.Latitude,
                    Longitude = node.Longitude,
                    Name = node.Name
                };
                result.Nodes.Add(tnode);
                var pingRequest = CreateUriBase(node.Address) + CreatePingUriParameter(parameter.Ip);
                var pingTask = MakeRequest(pingRequest);
                taskList.Add(pingTask);
            }
            foreach (var task in taskList)
            {
                var reply = await task;
                result.Replies.Add(reply);
            }
            return result;
        }

        /// <summary>
        /// Makes the request.
        /// </summary>
        /// <param name="pingRequest">The ping request.</param>
        /// <returns></returns>
        /// <exception cref="System.NotImplementedException"></exception>
        private async Task<PingReply> MakeRequest(string pingRequest)
        {
            try
            {
                var request = WebRequest.CreateHttp(pingRequest);
                using (var response = (await request.GetResponseAsync()) as HttpWebResponse)
                {
                    if(response==null)
                        throw new Exception(String.Format(
                            "Connection error! Response is null!"));
                    if (response.StatusCode != HttpStatusCode.OK)
                        throw new Exception(String.Format(
                            "Server error (HTTP {0}: {1}).",
                            response.StatusCode,
                            response.StatusDescription));
                    var jsonSerializer = new DataContractJsonSerializer(typeof(PingReply));
                    var responseStream = response.GetResponseStream();
                    if (responseStream==null) throw new Exception(String.Format("Connection error! Response stream is null!"));
                    var objResponse = jsonSerializer.ReadObject(responseStream);
                    var jsonResponse = objResponse as PingReply;
                    return jsonResponse;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return null;
            }
        }

        /// <summary>
        /// FPings the specified parameter.
        /// </summary>
        /// <param name="parameter">The parameter.</param>
        /// <returns></returns>
        /// <exception cref="System.NotImplementedException"></exception>
        public FPingResult FPing(SpotterDataTransferObject.FPingParameter parameter)
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// Updates the specified node.
        /// </summary>
        /// <param name="nodeName">Name of the node.</param>
        /// <param name="nodeAddress">The node address.</param>
        /// <returns></returns>
        public string Update(string nodeName, string nodeAddress)
        {
            try
            {
                var node = _entities.Nodes.SingleOrDefault(n => n.Name == nodeName);
                node.Address = nodeAddress;
                node.LastCheckin = DateTime.Now;
                _entities.SaveChanges();
                return "Success!";
            }
            catch (Exception exception)
            {
                return "Fail! " + exception.Message;
            }

        }

        /// <summary>
        /// Creates the ping URI parameter.
        /// </summary>
        /// <param name="ip">The ip.</param>
        /// <returns></returns>
        private static string CreatePingUriParameter(String ip)
        {
            return "ping/\u0022" + ip + "\u0022";
        }

        /// <summary>
        /// Creates the fping URI parameter.
        /// </summary>
        /// <param name="ipList">The ip list.</param>
        /// <returns></returns>
        private static string CreateFpingUriParameter(IReadOnlyCollection<string> ipList)
        {
            var result = ipList.Aggregate("fping/[", (current, ip) => current + ("\"" + ip + "\","));
            if (ipList.Count != 0)
            {
                result = result.Substring(0, result.Length - 2); //levesszük az utolsó ','-t
            }
            result += "]";
            return result;
        }

        /// <summary>
        /// Creates the URI base.
        /// </summary>
        /// <param name="address">The address.</param>
        /// <returns></returns>
        private static string CreateUriBase(String address)
        {
            return "http://" + address + ":8080/";
        }
    }
}
