include_recipe "build-essential"

# First install standard nginx, then upgrade version through source
package "nginx"

# Compile fresh version from nginx.org
version = node[:nginx][:version]
compile_flags = [
    "--prefix=#{node[:nginx][:prefix]}",
    "--conf-path=#{node[:nginx][:conf]}/nginx.conf",
    "--error-log-path=#{node[:nginx][:logs]}/error.log",
    "--http-log-path=#{node[:nginx][:logs]}/access.log",
    "--with-http_ssl_module",
    "--with-http_gzip_static_module"
].join(" ")

remote_file "#{Chef::Config[:file_cache_path]}/nginx-#{version}.tar.gz" do
    source "http://nginx.org/download/nginx-#{version}.tar.gz"
    action :create_if_missing
end

bash "compile_nginx_source" do
    cwd Chef::Config[:file_cache_path]
    code <<-EOH
        tar zxf nginx-#{version}.tar.gz
        cd nginx-#{version} && ./configure #{compile_flags}
        make && make install
    EOH
    creates "/usr/local/sbin/nginx" 
end

directory "#{node[:nginx][:conf]}/conf.d" do
    owner "root"
    group "root"
    mode "0644"
end

directory "#{node[:nginx][:conf]}/sites-enabled" do
    owner "root"
    group "root"
    mode "0644"
end

service "nginx" do
    supports :status => true, :restart => true, :reload => true
    action :enable
    subscribes :restart, resources(:bash => "compile_nginx_source")
end

template "nginx.conf" do
    path "#{node[:nginx][:conf]}/nginx.conf"
    source "nginx.conf.erb"
    owner "root"
    group "root"
    mode "0644"
    notifies :restart, resources(:service => "nginx"), :immediately
end

template "default" do 
    path "#{node[:nginx][:conf]}/sites-enabled/default"
    source "default.erb"
    owner "root"
    group "root"
    mode "0644"
    notifies :restart, resources(:service => "nginx"), :immediately
end


